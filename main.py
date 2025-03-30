import typer
from typing_extensions import Annotated
import re
from src.phishing_detector import detect_phishing
from src.db import DB
from src.db_types import Flag

app = typer.Typer()
db = DB()

src_email_regex = r"Suspicious email domain:"
src_body_regex = r"Suspicious phrase:"

@app.command()
def check(sender: str, recipient: str, body: str):
    res = detect_phishing(sender, body)
    if(res["isPhishing"]):
        violations = res["violations"]
        flags: list[Flag] = []
        for (reason, section) in violations:
            if re.search(src_email_regex, reason):
                re_match = re.search(section, sender)
                if(re_match == None):
                    raise LookupError("It blew up")
                fr = re_match.start()
                to = re_match.end()
                flags.append(Flag(None, None, "email", fr, to, reason))# Insert into flags
            elif re.search(src_body_regex, reason):
                re_match = re.search(section, body)
                if(re_match == None):
                    raise LookupError("It blew up")
                fr = re_match.start()
                to = re_match.end()
                flags.append(Flag(None, None, "body", fr, to, reason))

        db.insert(sender,recipient,body,flags)
    print(res)
    return res

@app.command()
def list(sender: str | None = None):
    if(sender):
        return db.select(sender=sender)
    return db.select()

@app.command()
def pretty():
    pass


if __name__ == '__main__':
    app()