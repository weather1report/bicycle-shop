from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from urllib.request import ProxyHandler, build_opener

root = Path(__file__).resolve().parent
python = root / 'backend/.venv/Scripts/python.exe'
npm = shutil.which('npm.cmd')
node = shutil.which('node.exe')
http = build_opener(ProxyHandler({}))


def stop(process):
    if process.poll() is None:
        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait(timeout=10)


def execute(command, message, cwd=None):
    print(message, flush=True)
    with tempfile.TemporaryFile() as output:
        process = subprocess.Popen(command, cwd=cwd, stdout=output, stderr=output, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        try:
            code = process.wait(timeout=600)
            if code:
                output.seek(0)
                details = output.read().decode('utf-8', errors='replace').strip()
                raise RuntimeError('Не удалось подготовить зависимости.\n' + details[-4000:])
        except subprocess.TimeoutExpired:
            raise RuntimeError('Установка заняла больше 10 минут. Проверьте интернет и повторите запуск.') from None
        finally:
            stop(process)


def wait_for_site(processes):
    pending = ['http://127.0.0.1:8000/api/health', 'http://127.0.0.1:5173/', 'http://127.0.0.1:5173/api/health']
    deadline = time.monotonic() + 45
    while pending and time.monotonic() < deadline:
        if any(process.poll() is not None for process in processes):
            raise RuntimeError('Сервер завершился при запуске. Причина ошибки указана выше.')
        for url in pending[:1]:
            try:
                with http.open(url, timeout=1) as response:
                    if response.status == 200:
                        pending.remove(url)
            except OSError:
                pass
        if pending:
            time.sleep(0.3)
    if pending:
        raise RuntimeError('Магазин не ответил за 45 секунд. Проверьте ошибки выше. Не отвечает: ' + ', '.join(sorted(pending)))


def run():
    if sys.platform != 'win32':
        raise RuntimeError('Этот файл запуска предназначен для Windows.')
    print('Подготовка магазина…', flush=True)
    if sys.version_info < (3, 12):
        raise RuntimeError('Установите Python 3.12 или новее.')
    if not npm or not node:
        raise RuntimeError('Установите Node.js с npm и откройте терминал заново.')
    version = subprocess.check_output([node, '--version'], text=True, timeout=10).strip().lstrip('v')
    major, minor, *_ = map(int, version.split('.'))
    if not ((major == 20 and minor >= 19) or (major == 22 and minor >= 12) or major > 22):
        raise RuntimeError('Нужен Node.js 20.19+ в ветке 20, либо 22.12 или новее.')
    for port in (8000, 5173):
        with socket.socket() as check:
            try:
                check.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
                check.bind(('127.0.0.1', port))
            except OSError:
                raise RuntimeError(f'Порт {port} недоступен. Остановите предыдущий запуск через Ctrl+C.') from None
    if not python.exists():
        execute([sys.executable, '-m', 'venv', str(root / 'backend/.venv')], 'Создание окружения Python…')
    installed = subprocess.run([str(python), '-c', 'import fastapi, sqlmodel, uvicorn, email_validator'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
    if installed.returncode:
        execute([str(python), '-m', 'pip', 'install', '--quiet', '--disable-pip-version-check', '-r', str(root / 'backend/requirements.txt')], 'Установка зависимостей Python. При первом запуске потребуется интернет…')
    if not (root / 'frontend/node_modules/vite/bin/vite.js').exists():
        execute([npm, 'ci', '--silent', '--no-audit', '--no-fund'], 'Установка зависимостей сайта. Это может занять несколько минут…', cwd=root / 'frontend')
    processes = []
    try:
        print('Запуск серверов и проверка готовности…', flush=True)
        options = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP, 'stdout': subprocess.DEVNULL}
        processes.append(subprocess.Popen([str(python), '-m', 'uvicorn', 'main:app', '--reload', '--host', '127.0.0.1', '--port', '8000', '--no-access-log', '--log-level', 'error'], cwd=root / 'backend', **options))
        processes.append(subprocess.Popen([node, 'node_modules/vite/bin/vite.js', '--host', '127.0.0.1', '--port', '5173', '--strictPort', '--logLevel', 'error'], cwd=root / 'frontend', **options))
        wait_for_site(processes)
        print('\nМагазин готов: http://127.0.0.1:5173\nОткройте эту ссылку в браузере.\nОставьте терминал открытым. Для остановки нажмите Ctrl+C.\n', flush=True)
        while all(process.poll() is None for process in processes):
            time.sleep(0.5)
        raise RuntimeError('Одна из частей магазина остановилась. Проверьте сообщение об ошибке выше.')
    finally:
        for process in processes:
            stop(process)


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('\nМагазин остановлен.', flush=True)
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(f'Ошибка запуска: {error}', file=sys.stderr, flush=True)
        sys.exit(1)
