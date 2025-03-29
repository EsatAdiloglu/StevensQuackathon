import typer
import re
from phishing_detector import detect_phishing
from db import DB
from db_types import Flag

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
    return res

@app.command()
def list_report(sender: str | None):
    if(sender):
        return db.select(sender=sender)
    return db.select()

@app.command()
def pretty():
    pass


if __name__ == '__main__':
    app()