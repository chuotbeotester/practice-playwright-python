import datetime
from typing import Dict, Union
from dateutil.relativedelta import relativedelta
from .datetime_helper import DateType


class DateHelper:
    """Lớp tiện ích hỗ trợ xử lý Ngày (Date) không bao gồm thời gian."""

    # Định dạng ngày mặc định
    DEFAULT_FORMAT = "%d/%m/%Y"

    @staticmethod
    def get_time(date_type: DateType) -> str:
        """
        Lấy mốc ngày chuẩn theo DateType.

        Args:
            date_type (DateType): Mốc ngày (YESTERDAY, TODAY, TOMORROW).

        Returns:
            str: Chuỗi ngày chuẩn theo định dạng DEFAULT_FORMAT.
            
        Raises:
            ValueError: Nếu date_type không hợp lệ.
        """
        today = datetime.date.today()

        if date_type == DateType.TODAY:
            target_date = today
        elif date_type == DateType.YESTERDAY:
            target_date = today - datetime.timedelta(days=1)
        elif date_type == DateType.TOMORROW:
            target_date = today + datetime.timedelta(days=1)
        else:
            raise ValueError(f"Loại ngày không hỗ trợ: {date_type}")

        return target_date.strftime(DateHelper.DEFAULT_FORMAT)

    @staticmethod
    def build_time(
        day: int, month: int, year: int, custom_format: str = None
    ) -> str:
        """
        Lắp ráp chuỗi ngày từ các con số.

        Args:
            day (int): Ngày.
            month (int): Tháng.
            year (int): Năm.
            custom_format (str, optional): Định dạng tùy chỉnh, nếu None sẽ dùng định dạng mặc định.

        Returns:
            str: Chuỗi ngày đã định dạng.

        Raises:
            ValueError: Nếu các tham số không tạo thành một mốc ngày hợp lệ.
        """
        try:
            target_date = datetime.date(year, month, day)
        except ValueError as e:
            raise ValueError(f"Các thông số ngày không hợp lệ: {e}")

        fmt = custom_format if custom_format else DateHelper.DEFAULT_FORMAT
        return target_date.strftime(fmt)

    @staticmethod
    def change_format(date_str: str, current_format: str, new_format: str) -> str:
        """
        Chuyển đổi chuỗi ngày sang định dạng mới.

        Args:
            date_str (str): Chuỗi ngày cần chuyển đổi.
            current_format (str): Định dạng hiện tại.
            new_format (str): Định dạng đích cần chuyển.

        Returns:
            str: Chuỗi ngày ở định dạng mới.
        """
        dt = DateHelper.to_native(date_str, current_format)
        return dt.strftime(new_format)

    @staticmethod
    def to_default_format(date_str: str, current_format: str) -> str:
        """
        Ép chuỗi ngày về định dạng mặc định của lớp.

        Args:
            date_str (str): Chuỗi ngày đầu vào.
            current_format (str): Định dạng hiện tại của chuỗi.

        Returns:
            str: Chuỗi ngày định dạng mặc định.
        """
        return DateHelper.change_format(
            date_str, current_format, DateHelper.DEFAULT_FORMAT
        )

    @staticmethod
    def add_time(
        date_str: str, current_format: str, years: int = 0, months: int = 0, days: int = 0
    ) -> str:
        """
        Dịch chuyển ngày cộng hoặc trừ.

        Args:
            date_str (str): Chuỗi ngày cần dịch chuyển.
            current_format (str): Định dạng của chuỗi.
            years (int): Số năm cần cộng (trừ nếu âm).
            months (int): Số tháng cần cộng (trừ nếu âm).
            days (int): Số ngày cần cộng (trừ nếu âm).

        Returns:
            str: Chuỗi ngày đã được dịch chuyển.
        """
        dt = DateHelper.to_native(date_str, current_format)
        new_dt = dt + relativedelta(years=years, months=months, days=days)
        return new_dt.strftime(current_format)

    @staticmethod
    def extract_parts(
        date_str: str, current_format: str
    ) -> Dict[str, Dict[str, Union[str, int]]]:
        """
        Bóc tách chuỗi ngày thành các thành phần rời rạc.

        Args:
            date_str (str): Chuỗi ngày cần bóc tách.
            current_format (str): Định dạng của chuỗi.

        Returns:
            dict: Chứa thông tin năm, tháng, ngày dưới dạng str và int.
        """
        dt = DateHelper.to_native(date_str, current_format)

        return {
            "str": {
                "year": dt.strftime("%Y"),
                "month": dt.strftime("%m"),
                "day": dt.strftime("%d"),
            },
            "int": {
                "year": dt.year,
                "month": dt.month,
                "day": dt.day,
            },
        }

    @staticmethod
    def to_native(date_str: str, current_format: str) -> datetime.date:
        """
        Phân tích chuỗi ngày thành đối tượng date của Python.

        Args:
            date_str (str): Chuỗi ngày gốc.
            current_format (str): Định dạng của chuỗi.

        Returns:
            datetime.date: Đối tượng ngày nguyên bản.

        Raises:
            ValueError: Nếu chuỗi không tuân thủ định dạng đã cho.
        """
        try:
            return datetime.datetime.strptime(date_str, current_format).date()
        except ValueError as e:
            raise ValueError(
                f"Lỗi cú pháp ngày. Chuỗi '{date_str}' không khớp với format '{current_format}'. Chi tiết: {e}"
            )