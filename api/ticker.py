import threading
import logging
from kiteconnect import KiteTicker

logger = logging.getLogger(__name__)


class TickerManager:
    """
    Manages a KiteTicker WebSocket connection to stream live LTPs.
    Runs in a background thread; stores latest LTP per instrument token.
    Use get_ltp(instrument_token) to fetch the latest price.
    """

    def __init__(self):
        self.api_key: str | None = None
        self.access_token: str | None = None
        self.ticker: KiteTicker | None = None
        self._ltp_store: dict[int, float] = {}   # {instrument_token: ltp}
        self._subscribed_tokens: list[int] = []
        self._thread: threading.Thread | None = None
        self._running = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(self, api_key: str, access_token: str, instrument_tokens: list[int]):
        """
        Start (or restart) the ticker with a fresh access token and token list.
        Safe to call multiple times – stops the old connection first.
        """
        self.stop()

        self.api_key = api_key
        self.access_token = access_token
        self._subscribed_tokens = instrument_tokens
        self._ltp_store = {}
        self._running = True

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info(f"TickerManager started for {len(instrument_tokens)} instruments.")

    def stop(self):
        """Gracefully stop the WebSocket connection."""
        self._running = False
        if self.ticker:
            try:
                self.ticker.stop()
            except Exception:
                pass
            self.ticker = None
        logger.info("TickerManager stopped.")

    def get_ltp(self, instrument_token: int) -> float | None:
        """Return the latest LTP for a token, or None if not yet received."""
        return self._ltp_store.get(instrument_token)

    def update_subscriptions(self, instrument_tokens: list[int]):
        """
        Subscribe to additional / updated instrument tokens on a live connection.
        Useful when holdings change without restarting the whole ticker.
        """
        self._subscribed_tokens = instrument_tokens
        if self.ticker and self._running:
            try:
                self.ticker.subscribe(instrument_tokens)
                self.ticker.set_mode(self.ticker.MODE_LTP, instrument_tokens)
                logger.info(f"Updated subscriptions: {instrument_tokens}")
            except Exception as e:
                logger.error(f"Failed to update subscriptions: {e}")

    @property
    def is_running(self) -> bool:
        return self._running and self._thread is not None and self._thread.is_alive()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _run(self):
        self.ticker = KiteTicker(api_key=self.api_key, access_token=self.access_token)

        # --- Callbacks ---

        def on_connect(ws, response):
            logger.info("KiteTicker connected.")
            if self._subscribed_tokens:
                ws.subscribe(self._subscribed_tokens)
                ws.set_mode(ws.MODE_LTP, self._subscribed_tokens)

        def on_ticks(ws, ticks):
            for tick in ticks:
                token = tick["instrument_token"]
                ltp = tick.get("last_price")
                if ltp is not None:
                    self._ltp_store[token] = ltp

        def on_close(ws, code, reason):
            logger.warning(f"KiteTicker closed: {code} – {reason}")
            self._running = False

        def on_error(ws, code, reason):
            logger.error(f"KiteTicker error: {code} – {reason}")

        self.ticker.on_connect = on_connect
        self.ticker.on_ticks = on_ticks
        self.ticker.on_close = on_close
        self.ticker.on_error = on_error

        # reconnect=True lets KiteTicker handle drops automatically
        self.ticker.connect(threaded=False, reconnect=True, max_delay=5, max_tries=10)


# ---------------------------------------------------------------------------
# Singleton – import this instance everywhere
# ---------------------------------------------------------------------------
ticker_manager = TickerManager()
