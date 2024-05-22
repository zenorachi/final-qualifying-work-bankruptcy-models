import asyncio
import settings as st
from company import Company
import matplotlib.pyplot as plt


def make_plot(x, y, y_label: str, title: str):
    """
    X - Years
    Y - Altman Z-Scores / Fulmer score
    """

    plt.plot(x, y, color='green', marker='o', markersize=7)
    for i, value in enumerate(y):
        plt.annotate(str(value), (x[i], value), textcoords="offset points", xytext=(5, 0), ha='left')
    plt.xlabel('Год')
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(x)
    plt.show()


if __name__ == '__main__':
    settings: st.Settings = st.get_settings()
    cmp: Company = Company(settings=settings)
    asyncio.run(cmp())

    years, y1, y2, y3, y4 = [2020, 2021, 2022], [], [], [], []

    for year in years:
        y1.append(cmp.get_z2_altman_score(str(year)))
        y2.append(cmp.get_z4_altman_score(str(year)))
        y3.append(cmp.get_z5_altman_score(str(year)))
        y4.append(cmp.get_fulmer_score(str(year)))

    make_plot(years, y1, 'Счет Альтмана', 'Двухфакторная модель Альтмана')
    make_plot(years, y2, 'Cчет Альтмана', 'Четырехфакторная модель Альтмана')
    make_plot(years, y3, 'Счет Альтмана', 'Пятифакторная модель Альтмана')
    make_plot(years, y4, 'Счет Фулмера', 'Модель Фулмера')

