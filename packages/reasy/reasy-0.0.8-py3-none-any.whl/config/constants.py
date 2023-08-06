from pathlib import Path


class Constants:
    coding = 'utf-8'

    bt7086_url = 'http://bt7086.org/pw'

    user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Mobile Safari/537.36'

    @staticmethod
    def project_root_path():
        return str(Path(__file__).parent.parent)
