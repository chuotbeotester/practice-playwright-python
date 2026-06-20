import warnings
import logging
from enum import Enum


class FailureHandling(Enum):
    """
    Enum định nghĩa cách xử lý lỗi trong các keyword của framework.

    - STOP_ON_FAILURE  : Dừng test case ngay lập tức khi gặp lỗi (mặc định).
    - CONTINUE_ON_FAILURE : Ghi log lỗi nhưng test case vẫn tiếp tục chạy.
    - OPTIONAL         : Chỉ ghi warning, bỏ qua lỗi (dùng cho popup tùy chọn).
    """

    STOP_ON_FAILURE = "stop_on_failure"
    CONTINUE_ON_FAILURE = "continue_on_failure"
    OPTIONAL = "optional"


def handle_failure(action: str, error: Exception, flow_control: FailureHandling, logger: logging.Logger = None,) -> None:
    """
    Hàm xử lý lỗi tập trung — dùng chung cho BasePage, BaseApi và bất kỳ layer nào khác.

    Args:
        action      : Tên hàm/action đang thực hiện khi xảy ra lỗi (để log).
        error       : Exception bắt được.
        flow_control: Mức độ xử lý lỗi (STOP / CONTINUE / OPTIONAL).
        logger      : Logger instance của caller. Nếu None, dùng root logger.

    Behavior:
        - STOP_ON_FAILURE    → log ERROR rồi raise exception, test case FAIL ngay.
        - CONTINUE_ON_FAILURE → chỉ log ERROR, test case tiếp tục chạy.
        - OPTIONAL           → chỉ log WARNING, test case tiếp tục.
    """
    if logger is not None:
        _logger = logger
    else:
        _logger = logging.getLogger(__name__)

    if flow_control == FailureHandling.STOP_ON_FAILURE:
        _logger.error(f"[STOP_ON_FAILURE] {action} — {error}")
        raise error

    elif flow_control == FailureHandling.CONTINUE_ON_FAILURE:
        _logger.error(f"[CONTINUE_ON_FAILURE] {action} — {error}")

    elif flow_control == FailureHandling.OPTIONAL:
        _logger.warning(f"[OPTIONAL] {action} — {error}")
        warnings.warn(f"[OPTIONAL] {action}: {error}", UserWarning, stacklevel=3)