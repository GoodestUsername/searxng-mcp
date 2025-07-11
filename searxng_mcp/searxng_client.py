import csv
import json
from enum import Enum
from inspect import Parameter, signature
from io import StringIO
from typing import Annotated, Any, Callable, Literal

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.tools.tool import ToolResult
from httpx import AsyncClient
from mcp.types import TextContent
from pydantic import Field


class Categories(Enum):
    general = "general"
    images = "images"
    videos = "videos"
    news = "news"
    map = "map"
    music = "music"
    it = "it"
    science = "science"
    files = "files"
    social_media = "social_media"


class Engines(Enum):
    m_1337x = "1337x"
    m_360search = "360search"
    m_360search_videos = "360search_videos"
    m_9gag = "9gag"
    acfun = "acfun"
    adobe_stock = "adobe_stock"
    ahmia = "ahmia"
    alpinelinux = "alpinelinux"
    annas_archive = "annas_archive"
    ansa = "ansa"
    apkmirror = "apkmirror"
    apple_app_store = "apple_app_store"
    apple_maps = "apple_maps"
    archlinux = "archlinux"
    artic = "artic"
    arxiv = "arxiv"
    ask = "ask"
    astrophysics_data_system = "astrophysics_data_system"
    baidu = "baidu"
    bandcamp = "bandcamp"
    base = "base"
    bilibili = "bilibili"
    bing = "bing"
    bing_images = "bing_images"
    bing_news = "bing_news"
    bing_videos = "bing_videos"
    bitchute = "bitchute"
    bpb = "bpb"
    brave = "brave"
    bt4g = "bt4g"
    btdigg = "btdigg"
    ccc_media = "ccc_media"
    chefkoch = "chefkoch"
    chinaso = "chinaso"
    cloudflareai = "cloudflareai"
    command = "command"
    core = "core"
    cppreference = "cppreference"
    crates = "crates"
    crossref = "crossref"
    currency_convert = "currency_convert"
    dailymotion = "dailymotion"
    deepl = "deepl"
    deezer = "deezer"
    demo_offline = "demo_offline"
    demo_online = "demo_online"
    destatis = "destatis"
    deviantart = "deviantart"
    dictzone = "dictzone"
    digbt = "digbt"
    discourse = "discourse"
    docker_hub = "docker_hub"
    doku = "doku"
    duckduckgo = "duckduckgo"
    duckduckgo_definitions = "duckduckgo_definitions"
    duckduckgo_extra = "duckduckgo_extra"
    duckduckgo_weather = "duckduckgo_weather"
    duden = "duden"
    dummy_offline = "dummyoffline"
    dummy = "dummy"
    ebay = "ebay"
    elasticsearch = "elasticsearch"
    emojipedia = "emojipedia"
    fdroid = "fdroid"
    findthatmeme = "findthatmeme"
    flickr = "flickr"
    flickr_noapi = "flickr_noapi"
    freesound = "freesound"
    frinkiac = "frinkiac"
    fyyd = "fyyd"
    geizhals = "geizhals"
    genius = "genius"
    gitea = "gitea"
    github = "github"
    gitlab = "gitlab"
    goodreads = "goodreads"
    google = "google"
    google_images = "google_images"
    google_news = "google_news"
    google_play = "google_play"
    google_scholar = "google_scholar"
    google_videos = "google_videos"
    hackernews = "hackernews"
    hex = "hex"
    huggingface = "huggingface"
    il_post = "il_post"
    imdb = "imdb"
    imgur = "imgur"
    ina = "ina"
    invidious = "invidious"
    ipernity = "ipernity"
    iqiyi = "iqiyi"
    jisho = "jisho"
    json_engine = "json_engine"
    kickass = "kickass"
    lemmy = "lemmy"
    lib_rs = "lib_rs"
    libretranslate = "libretranslate"
    lingva = "lingva"
    livespace = "livespace"
    loc = "loc"
    mariadb_server = "mariadb_server"
    mastodon = "mastodon"
    material_icons = "material_icons"
    mediathekviewweb = "mediathekviewweb"
    mediawiki = "mediawiki"
    meilisearch = "meilisearch"
    metacpan = "metacpan"
    microsoft_learn = "microsoft_learn"
    mixcloud = "mixcloud"
    mojeek = "mojeek"
    mongodb = "mongodb"
    moviepilot = "moviepilot"
    mozhi = "mozhi"
    mrs = "mrs"
    mullvad_leta = "mullvad_leta"
    mwmbl = "mwmbl"
    mysql_server = "mysql_server"
    naver = "naver"
    niconico = "niconico"
    npm = "npm"
    nyaa = "nyaa"
    odysee = "odysee"
    ollama = "ollama"
    open_meteo = "open_meteo"
    openclipart = "openclipart"
    openlibrary = "openlibrary"
    opensemantic = "opensemantic"
    openstreetmap = "openstreetmap"
    openverse = "openverse"
    pdbe = "pdbe"
    peertube = "peertube"
    photon = "photon"
    pinterest = "pinterest"
    piped = "piped"
    piratebay = "piratebay"
    pixabay = "pixabay"
    pixiv = "pixiv"
    pkg_go_dev = "pkg_go_dev"
    podcastindex = "podcastindex"
    postgresql = "postgresql"
    presearch = "presearch"
    public_domain_image_archive = "public_domain_image_archive"
    pubmed = "pubmed"
    pypi = "pypi"
    quark = "quark"
    qwant = "qwant"
    radio_browser = "radio_browser"
    recoll = "recoll"
    reddit = "reddit"
    redis_server = "redis_server"
    reuters = "reuters"
    rottentomatoes = "rottentomatoes"
    rumble = "rumble"
    scanr_structures = "scanr_structures"
    searchcode_code = "searchcode_code"
    searx_engine = "searx_engine"
    seekr = "seekr"
    selfhst = "selfhst"
    semantic_scholar = "semantic_scholar"
    senscritique = "senscritique"
    sepiasearch = "sepiasearch"
    seznam = "seznam"
    sogou = "sogou"
    sogou_images = "sogou_images"
    sogou_videos = "sogou_videos"
    sogou_wechat = "sogou_wechat"
    solidtorrents = "solidtorrents"
    solr = "solr"
    soundcloud = "soundcloud"
    spotify = "spotify"
    springer = "springer"
    sqlite = "sqlite"
    stackexchange = "stackexchange"
    startpage = "startpage"
    steam = "steam"
    stract = "stract"
    svgrepo = "svgrepo"
    tagesschau = "tagesschau"
    tineye = "tineye"
    tokyotoshokan = "tokyotoshokan"
    tootfinder = "tootfinder"
    torznab = "torznab"
    translated = "translated"
    tubearchivist = "tubearchivist"
    unsplash = "unsplash"
    uxwing = "uxwing"
    vimeo = "vimeo"
    voidlinux = "voidlinux"
    wallhaven = "wallhaven"
    wikicommons = "wikicommons"
    wikidata = "wikidata"
    wikipedia = "wikipedia"
    wolframalpha_api = "wolframalpha_api"
    wolframalpha_noapi = "wolframalpha_noapi"
    wordnik = "wordnik"
    wttr = "wttr"
    www1x = "www1x"
    xpath = "xpath"
    yacy = "yacy"
    yahoo = "yahoo"
    yahoo_news = "yahoo_news"
    yandex = "yandex"
    yandex_music = "yandex_music"
    yep = "yep"
    youtube_api = "youtube_api"
    youtube_noapi = "youtube_noapi"
    yummly = "yummly"
    zlibrary = "zlibrary"


class Plugins(Enum):
    hash_plugin = "Hash_plugin"
    self_information = "Self_Information"
    tracker_url_remover = "Tracker_URL_remover"
    ahmia_blacklist = "Ahmia_blacklist"
    hostnames_plugin = "Hostnames_plugin"
    open_access_doi_rewrite = "Open_Access_DOI_rewrite"
    vim_like_hotkeys = "Vim-like_hotkeys"
    tor_check_plugin = "Tor_check_plugin"


def parse_args(func: Callable[..., Any], raw_args: dict[str, Any]) -> dict[str, Any]:
    sig = signature(func)
    cleaned = {}

    for name, param in sig.parameters.items():
        if name not in raw_args:
            continue

        value = raw_args[name]
        is_optional = param.default is not Parameter.empty or getattr(
            param.annotation, "__origin__", None
        ) is type(None)

        is_empty = value in ("", [], None)

        if is_empty:
            if not is_optional:
                raise ToolError(f"{name!r} is required and cannot be empty.")
            continue

        if type(value).__name__ == "list":
            if all(isinstance(item, Enum) for item in value):
                value = ", ".join([item.value for item in value])
                pass

        cleaned[name] = value

    return cleaned


class SearxngClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    async def search(
        self,
        q: Annotated[
            str,
            Field(
                title="query",
                description="""
                    The search query. This string is passed to external search services.
                    Thus, SearXNG supports syntax of each search service. 
                    For example, site:github.com SearXNG is a valid query for Google. 
                    However, if simply the query above is passed to any search engine 
                    which does not filter its results based on this syntax, 
                    you might not get the results you wanted.
                """,
            ),
        ],
        categories: (
            Annotated[
                list[Categories],
                Field(description="List of the active search categories."),
            ]
            | None
        ) = None,
        engines: (
            Annotated[
                list[Engines],
                Field(description="List of the active search engines."),
            ]
            | None
        ) = None,
        language: (
            Annotated[
                str,
                Field(description="ISO language code."),
            ]
            | None
        ) = None,
        pageno: Annotated[
            int,
            Field(
                title="page_number", description="Page number of query result.", ge=1
            ),
        ] = 1,
        time_range: (
            Annotated[
                Literal["day", "month", "year"],
                Field(description="Time range of search for engines which support it."),
            ]
            | None
        ) = None,
        format: Annotated[
            Literal["html", "json", "csv", "rss"],
            Field(description="Output format of results. Defaults to json."),
        ] = "json",
        image_proxy: (
            Annotated[
                bool,
                Field(description="Proxy image results through SearXNG."),
            ]
            | None
        ) = None,
        safesearch: (
            Annotated[
                Literal[0, 1, 2],
                Field(
                    description="""
                        Filter search results of engines which support safe search.
                        Higher the number, the stricter the safety level.
                    """
                ),
            ]
            | None
        ) = None,
        enabled_plugins: (
            Annotated[
                list[Plugins],
                Field(
                    description="""
                        List of the enabled search plugins.
                        Defaults:
                            - Hash_plugin
                            - Self_Information
                            - Tracker_URL_remover
                            - Ahmia_blacklist
                    """
                ),
            ]
            | None
        ) = None,
        disabled_plugins: (
            Annotated[
                list[Plugins],
                Field(
                    description="""
                        List of the disabled search plugins.
                        Defaults:
                            - Hostnames_plugin
                            - Open_Access_DOI_rewrite
                            - Vim-like_hotkeys
                            - Tor_check_plugi
                    """
                ),
            ]
            | None
        ) = None,
        enabled_engines: (
            Annotated[
                list[Engines],
                Field(description="List of the enabled search engines."),
            ]
            | None
        ) = None,
        disabled_engines: (
            Annotated[
                list[Engines],
                Field(description="List of the disabled search engines."),
            ]
            | None
        ) = None,
    ) -> ToolResult:
        args = parse_args(self.search, locals())
        client = AsyncClient(base_url=self.api_url)
        response = await client.get("/search", params=args)
        response.raise_for_status()
        match format:
            case "json":
                return ToolResult(
                    structured_content=json.loads(response.text),
                )
            case "csv":
                f = StringIO(response.text)
                reader = csv.reader(f, delimiter=",")
                return ToolResult(
                    structured_content={"output": reader},
                )
        return ToolResult(TextContent(text=response.text, type="text"))
