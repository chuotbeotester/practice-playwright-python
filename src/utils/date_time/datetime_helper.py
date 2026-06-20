import datetime
from enum import Enum
from typing import Dict, Union
from dateutil.relativedelta import relativedelta


class DateType(Enum):
    """Định nghĩa các mốc thời gian cơ bản."""
    YESTERDAY = "yesterday"
    TODAY = "today"
    TOMORROW = "tomorrow"


class DateTimeHelper:
    """Lớp tiện ích hỗ trợ xử lý Ngày & Giờ (DateTime) cho Automation Test."""

    # Định dạng thời gian mặc định của hệ thống
    DEFAULT_FORMAT = "%d/%m/%Y %H:%M:%S"

    @staticmethod
    def get_time(date_type: DateType) -> str:
        """
        Lấy mốc thời gian chuẩn (Get Relative Time).
        TODAY: Trả về chính xác thời gian hiện hành.
        YESTERDAY, TOMORROW: Trả về thời gian làm tròn về đầu ngày (00:00:00).

        Args:
            date_type (DateType): Mốc thời gian (YESTERDAY, TODAY, TOMORROW).

        Returns:
            str: Chuỗi thời gian chuẩn theo định dạng DEFAULT_FORMAT.
            
        Raises:
            ValueError: Nếu date_type không hợp lệ.
        """
        now = datetime.datetime.now()

        if date_type == DateType.TODAY:
            target_time = now
        elif date_type == DateType.YESTERDAY:
            target_time = (now - datetime.timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        elif date_type == DateType.TOMORROW:
            target_time = (now + datetime.timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        else:
            raise ValueError(f"Loại thời gian không hỗ trợ: {date_type}")

        return target_time.strftime(DateTimeHelper.DEFAULT_FORMAT)

    @staticmethod
    def build_time(
        day: int, month: int, year: int, hour: int, minute: int, second: int, custom_format: str = None
    ) -> str:
        """
        Lắp ráp chuỗi thời gian từ các con số.

        Args:
            day (int): Ngày.
            month (int): Tháng.
            year (int): Năm.
            hour (int): Giờ.
            minute (int): Phút.
            second (int): Giây.
            custom_format (str, optional): Định dạng tùy chỉnh, nếu None sẽ dùng định dạng mặc định.

        Returns:
            str: Chuỗi thời gian đã định dạng.

        Raises:
            ValueError: Nếu các tham số không tạo thành một mốc thời gian hợp lệ.
        """
        try:
            target_time = datetime.datetime(year, month, day, hour, minute, second)
        except ValueError as e:
            raise ValueError(f"Các thông số thời gian không hợp lệ: {e}")

        fmt = custom_format if custom_format else DateTimeHelper.DEFAULT_FORMAT
        return target_time.strftime(fmt)

    @staticmethod
    def change_format(time_str: str, current_format: str, new_format: str) -> str:
        """
        Chuyển đổi chuỗi thời gian sang định dạng mới.

        Args:
            time_str (str): Chuỗi thời gian cần chuyển đổi.
            current_format (str): Định dạng hiện tại của chuỗi đầu vào.
            new_format (str): Định dạng đích cần xuất ra.

        Returns:
            str: Chuỗi thời gian với định dạng mới.
        """
        dt = DateTimeHelper.to_native(time_str, current_format)
        return dt.strftime(new_format)

    @staticmethod
    def to_default_format(time_str: str, current_format: str) -> str:
        """
        Ép chuỗi thời gian về định dạng mặc định của lớp.

        Args:
            time_str (str): Chuỗi thời gian đầu vào.
            current_format (str): Định dạng hiện tại của chuỗi.

        Returns:
            str: Chuỗi thời gian định dạng mặc định.
        """
        return DateTimeHelper.change_format(
            time_str, current_format, DateTimeHelper.DEFAULT_FORMAT
        )

    @staticmethod
    def add_time(
        time_str: str,
        current_format: str,
        years: int = 0,
        months: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
    ) -> str:
        """
        Dịch chuyển thời gian cộng hoặc trừ.

        Args:
            time_str (str): Chuỗi thời gian cần dịch chuyển.
            current_format (str): Định dạng của chuỗi thời gian đó.
            years (int): Số năm cần cộng (trừ nếu số âm).
            months (int): Số tháng cần cộng (trừ nếu số âm).
            days (int): Số ngày cần cộng (trừ nếu số âm).
            hours (int): Số giờ cần cộng (trừ nếu số âm).
            minutes (int): Số phút cần cộng (trừ nếu số âm).
            seconds (int): Số giây cần cộng (trừ nếu số âm).

        Returns:
            str: Chuỗi thời gian đã được dịch chuyển.
        """
        dt = DateTimeHelper.to_native(time_str, current_format)
        new_dt = dt + relativedelta(
            years=years,
            months=months,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
        )
        return new_dt.strftime(current_format)

    @staticmethod
    def extract_parts(
        time_str: str, current_format: str
    ) -> Dict[str, Dict[str, Union[str, int]]]:
        """
        Bóc tách chuỗi thời gian thành các thành phần rời rạc phục vụ test hoặc input.

        Args:
            time_str (str): Chuỗi thời gian.
            current_format (str): Định dạng của chuỗi.

        Returns:
            dict: Chứa các phần tử rời rạc dạng str và int.
        """
        dt = DateTimeHelper.to_native(time_str, current_format)

        return {
            "str": {
                "year": dt.strftime("%Y"),
                "month": dt.strftime("%m"),
                "day": dt.strftime("%d"),
                "hour": dt.strftime("%H"),
                "minute": dt.strftime("%M"),
                "second": dt.strftime("%S"),
            },
            "int": {
                "year": dt.year,
                "month": dt.month,
                "day": dt.day,
                "hour": dt.hour,
                "minute": dt.minute,
                "second": dt.second,
            },
        }

    @staticmethod
    def to_native(time_str: str, current_format: str) -> datetime.datetime:
        """
        Phân tích chuỗi thời gian thành đối tượng datetime gốc của Python.

        Args:
            time_str (str): Chuỗi thời gian gốc.
            current_format (str): Định dạng thời gian.

        Returns:
            datetime.datetime: Đối tượng nguyên bản.

        Raises:
            ValueError: Nếu chuỗi không tuân thủ định dạng đã cho.
        """
        try:
            return datetime.datetime.strptime(time_str, current_format)
        except ValueError as e:
            raise ValueError(
                f"Lỗi cú pháp thời gian. Chuỗi '{time_str}' không khớp với format '{current_format}'. Chi tiết: {e}"
            )