import database
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys


def plot_day(start_date):
    # database
    db = database.Database()

    # retrieve x and y values
    x, y = db.get_data(start_date, 'txs_hour')

    # plot labels appearance
    plt.plot(x, y)
    plt.xlabel('time in [UTC]')
    plt.ylabel('transactions/hour')
    plt.grid()

    # Set x axis to hours %H:%M
    hours = mdates.HourLocator()
    t_fmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_locator(hours)
    plt.gca().xaxis.set_major_formatter(t_fmt)
    plt.xlim([x[0], x[len(x)-1]])
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show and save plot
    plt.show()
    plt.savefig('myfig')


if __name__ == '__main__':
    try:
        date = sys.argv[1]
        plot_day(date)
    except Exception as e:
        print(e)
        print('Requires 1 agrument: <date>')
        print('Example: python plot.py 2018-07-06')
