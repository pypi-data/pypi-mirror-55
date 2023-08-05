import os
import tempfile


HERE = os.path.dirname(os.path.abspath(__file__))

def setup_desktop():
    # make a secure temporary directory for sockets
    # This is only readable, writeable & searchable by our uid
    sockets_dir = tempfile.mkdtemp()
    sockets_path = os.path.join(sockets_dir, 'vnc-socket')
    return {
        'command': [
            'websockify', '-v',
            '--web', os.path.join(HERE, 'share/web/noVNC-1.1.0'),
            '--heartbeat', '30',
            '5901',
            '--unix-target', sockets_path,
            '--',
            os.path.join(HERE, 'share/tigervnc/bin/vncserver'),
            '-verbose',
            '-xstartup', os.path.join(HERE, 'share/xstartup'),
            '-geometry', '1024x768',
            '-SecurityTypes', 'None',
            '-rfbunixpath', sockets_path,
            '-fg',
            ':1',
        ],
        'port': 5901,
        'timeout': 30,
        'mappath': {'/': '/vnc_lite.html'},
    }
