import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "location,date_from,date_to,status_code,detail",
    [
        ("Алтай", "2024-05-19", "2024-06-02", 200, None),
        ("Алтай", "2024-05-19", "2024-06-29", 400, "Время бронирования больше 30 дней"),
        ("Алтай", "2024-06-02", "2024-05-19", 400, "Дата выезда меньше даты заезда"),
    ],
)
async def test_get_hotels_by_location_and_time(
    location, date_from, date_to, status_code, detail, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.get(
        f"/hotels/{location}",
        params={
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code
    if str(status_code).startswith("4"):
        assert response.json()["detail"] == detail
