from cishu.cishubase import cishubase
from myutils.utils import get_element_by, localcachehelper
import re


class japandict(cishubase):
    backgroundparser = """document.querySelectorAll('.lunajapandictcsswrapper').forEach((ele) => {
                ele.style.backgroundColor = {color}
                ele.querySelectorAll('.list-group-item').forEach((ele) => {
                    ele.style.backgroundColor = {color}
                })
            });"""

    def init(self):
        self.style = localcachehelper("cishucss/japandict")
        self.klass = "lunajapandictcsswrapper"

    def search(self, word):
        url = "https://www.japandict.com/"
        params = {"s": word, "lang": "eng", "list": 1}
        html = self.proxysession.get(url, params=params).text

        check = get_element_by("class", "alert-heading", html)
        if check:
            return
        res = get_element_by("class", "list-group list-group-flush", html)
        if not res:
            return
        res = re.sub('href="(.*?)"', 'href="https://www.japandict.com\\1"', res)
        res = re.sub('src="(.*?)"', 'src="https://www.japandict.com\\1"', res)

        csslink = "https://www.japandict.com/static/css/japandict.ac087f3ecbc8.css"

        if not self.style[csslink]:
            css = self.proxysession.get(csslink).text
            css = css.replace("padding-top:60px !important", "")
            css = self.parse_stylesheet(css, self.klass)
            self.style[csslink] = css

        # -----------------------------
        # DARK MODE INJECTION (UPDATED)
        # -----------------------------
        darkcss = """
        /* --- Forced Dark Theme for JapanDict (LunaTranslator) — Updated --- */

        .lunajapandictcsswrapper {
            background-color: #181818 !important;
            color: #f0f0f0 !important;
        }

        /* Make ALL text bright */
        .lunajapandictcsswrapper,
        .lunajapandictcsswrapper * {
            color: #f0f0f0 !important;
        }

        /* Explicit fixes for large text */
        .lunajapandictcsswrapper .xlarge,
        .lunajapandictcsswrapper .text-normal,
        .lunajapandictcsswrapper .me-4,
        .lunajapandictcsswrapper .kanji,
        .lunajapandictcsswrapper .kana,
        .lunajapandictcsswrapper h1,
        .lunajapandictcsswrapper h2,
        .lunajapandictcsswrapper h3,
        .lunajapandictcsswrapper h4,
        .lunajapandictcsswrapper h5,
        .lunajapandictcsswrapper h6,
        .lunajapandictcsswrapper .display-1,
        .lunajapandictcsswrapper .display-2,
        .lunajapandictcsswrapper .display-3,
        .lunajapandictcsswrapper .display-4,
        .lunajapandictcsswrapper .fw-bold,
        .lunajapandictcsswrapper .lead {
            color: #ffffff !important;
        }

        /* Links */
        .lunajapandictcsswrapper a {
            color: #8ab4f8 !important;
        }

        /* List items */
        .lunajapandictcsswrapper .list-group-item {
            background-color: #202020 !important;
            border-color: #333 !important;
        }

        /* General containers */
        .lunajapandictcsswrapper .bg-white,
        .lunajapandictcsswrapper .navbar,
        .lunajapandictcsswrapper .footer2,
        .lunajapandictcsswrapper .container-fluid,
        .lunajapandictcsswrapper .row {
            background-color: #181818 !important;
            color: #f0f0f0 !important;
        }

        /* Subtle borders */
        .lunajapandictcsswrapper * {
            border-color: #444 !important;
        }

        /* Remove unwanted elements */
        .lunajapandictcsswrapper .btn-feedback.btn-primary.btn,
        .lunajapandictcsswrapper .py-0.bg-white.navbar-light.navbar-expand-lg.fixed-top.smart-scroll.navbar-height.navbar,
        .lunajapandictcsswrapper .p-3.footer2.container-fluid,
        .lunajapandictcsswrapper .text-muted.small,
        .lunajapandictcsswrapper .pb-5.px-5.row,
        .lunajapandictcsswrapper .height-15 {
            display: none !important;
        }

        /* REMOVE THE NEW FOOTER */
        .lunajapandictcsswrapper footer,
        .lunajapandictcsswrapper footer *,
        .lunajapandictcsswrapper .footer.mt-auto,
        .lunajapandictcsswrapper .footer.mt-auto * {
            display: none !important;
        }
        """

        return '<style>{}{}</style><div class="{}">{}</div>'.format(
            self.style[csslink], darkcss, self.klass, res
        )

    def getUrl(self, word):
        return "https://www.japandict.com/?s={}&lang=eng&list=1".format(word)
