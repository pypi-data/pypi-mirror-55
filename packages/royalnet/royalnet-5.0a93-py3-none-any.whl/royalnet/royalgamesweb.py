"""The production Royalnet available at ryg.steffo.eu ."""

import os
from royalnet.web import create_app
from royalnet.web.royalprints import *


class TestConfig:
    DB_PATH = os.environ["DB_PATH"]
    TG_AK = os.environ["TG_AK"]
    SITE_NAME = "Royalnet"


app = create_app(TestConfig, [rp_home, rp_wikiview, rp_tglogin, rp_docs, rp_wikiedit, rp_mcstatus, rp_diarioview,
                              rp_profile, rp_login])


if __name__ == "__main__":
    app.run()
