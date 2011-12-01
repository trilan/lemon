import os

from gears.environment import Environment
from gears.finders import FileSystemFinder


lemon_dir = os.path.join(os.path.dirname(__file__), '..', 'lemon')

node_modules_dir = os.path.join(os.path.dirname(__file__), '..', 'node_modules')
os.environ['NODE_PATH'] = os.path.abspath(node_modules_dir)

dashboard_dir = os.path.abspath(os.path.join(lemon_dir, 'dashboard'))
dashboard_static_dir = os.path.join(dashboard_dir, 'static')
dashboard_assets_dir = os.path.join(dashboard_dir, 'assets')

dashboard_env = Environment(dashboard_static_dir)
dashboard_env.register_defaults()
dashboard_env.finders.register(FileSystemFinder([dashboard_assets_dir]))
dashboard_env.public_assets.register('dashboard/css/style.css')
dashboard_env.public_assets.register('dashboard/js/script.js')


extradmin_dir = os.path.abspath(os.path.join(lemon_dir, 'extradmin'))
extradmin_static_dir = os.path.join(extradmin_dir, 'static')
extradmin_assets_dir = os.path.join(extradmin_dir, 'assets')

extradmin_env = Environment(extradmin_static_dir)
extradmin_env.register_defaults()
extradmin_env.finders.register(FileSystemFinder([extradmin_assets_dir]))


if __name__ == '__main__':
    dashboard_env.save()
    extradmin_env.save()
