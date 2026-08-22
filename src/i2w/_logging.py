"""Debug logging setup with multiple verbosity levels.

Provides logger instances configured for different debug levels (0-3),
allowing fine-grained control over debugging output verbosity.
"""

import logging

logger = logging.LoggerAdapter(logging.getLogger(__name__))
logger_d1 = logging.LoggerAdapter(logging.getLogger(__name__), {"debug_level": 1})
logger_d2 = logging.LoggerAdapter(logging.getLogger(__name__), {"debug_level": 2})
logger_d3 = logging.LoggerAdapter(logging.getLogger(__name__), {"debug_level": 3})
