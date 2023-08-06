from time import sleep
import click

from timebox.lib.hue import *
from timebox.lib.sound import sound
from timebox.lib.support import plural


@click.command()
@click.option(
    "--time", "-t", default=45, help="Number of minuts for the timer",
    show_default=True
)
@click.option(
    "--beeps",
    "-b",
    default=3,
    help="Numbers of beeps to notify that the session is finished",
    show_default=True
)
@click.option(
    "--before_end",
    "-be",
    default=15,
    help="Notify with an alert X minutes before the session ends.",
    show_default=True
)
@click.option(
    "--beeps_in_session",
    "-bis",
    default=1,
    help="Number of beeps to notify you that there is X minutes left of session",
    show_default=True
)
def main(time, beeps, beeps_in_session, before_end):
    time = abs(time)
    if time > before_end:
        alert = time - before_end
        click.echo(
            info(
                f"You will be notified after {orange(alert)} {plural('minute', alert)}, and when the session ends after {orange(time)} {plural('minute', time)}"
            )
        )
        sleep(alert * 60)
        sound(beeps=beeps_in_session, seconds=1.15, seconds_between_beep=0)
        click.echo(
            run(
                f"It's {orange(before_end)} {plural('minute', before_end)} left of session"
            )
        )
        sleep((before_end * 60) - (beeps_in_session * 1.5))
        sound(beeps=beeps)
    else:
        click.echo(
            info(
                f"You will be notified when your session ends after {orange(time)} {plural('minute', time)}"
            )
        )
        sleep(time * 60)
        sound(beeps=beeps)
    click.echo(good("Hope your had an awesome session!"))


if __name__ == "__main__":
    main()

