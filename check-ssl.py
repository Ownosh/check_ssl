import ssl
import datetime


def get_ssl_expiry_date(hostname):
    conn = ssl.create_connection((hostname, 443))
    context = ssl.create_default_context()
    sock = context.wrap_socket(conn, server_hostname=hostname)
    cert = sock.getpeercert()
    expiry_date = cert['notAfter']
    expiry_date = datetime.datetime.strptime(expiry_date, '%b %d %H:%M:%S %Y GMT')
    expiry_date = expiry_date.replace(tzinfo=datetime.timezone.utc)
    return expiry_date


def time_until_ssl_expiry(hostname):
    current_date = datetime.datetime.now(datetime.timezone.utc)
    expiry_date = get_ssl_expiry_date(hostname)
    remaining_time = expiry_date - current_date
    return remaining_time


def main():
    hostname = input("Введите адрес сайта (например, example.com): ")
    try:
        remaining_time = time_until_ssl_expiry(hostname)
        if remaining_time.days > 0:
            print(
                f"До окончания срока действия SSL-сертификата осталось {remaining_time.days} "
                f"дней! Не забудьте обновить сертификат!")
        else:
            print(f"Срок действия SSL-сертификата истек {abs(remaining_time.days)} дней назад!")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
