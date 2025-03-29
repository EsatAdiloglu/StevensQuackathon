import typer
from phishing_detector import detect_phishing
from db import DB

app = typer.Typer()
db = DB()

@app.command()
def check(sender: str, recipient: str, body: str):
    res = detect_phishing(sender, body)
    if(res["isPhishing"]):
        violations = res["violations"]
        flags = []
        for (reason, section) in violations:
            pass # Insert into flags

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