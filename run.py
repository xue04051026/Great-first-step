from app import create_app, db
from app.models import User, basicInfo, Major

app = create_app()

# (推荐) 添加 shell 上下文，方便调试
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, basicInfo=basicInfo, Major=Major)

if __name__ == '__main__':
    app.run(debug=True)