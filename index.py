from myapp import create_app,initAdmin
app = create_app()
initAdmin()

if __name__ == '__main__':
    app.run(debug=True)
 