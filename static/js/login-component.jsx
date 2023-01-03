const LoginForm = () => {
    return (
    <section>
        <h3 className="mb-4 pb-2 pb-md-0 mb-md-5 px-md-2">Log in</h3>
        <form action="/login" method="POST" className="px-md-2" >
        <div className="form-outline mb-4">
            <input type="text" id="login-email" name="email" className="form-control" />
            <label className="form-label">Email</label>
            <input type="password" id="login-password" name="password" className="form-control" />
            <label className="form-label">Password</label>
            <div><input type="submit" value="Login"/></div>
        </div>
        </form>
    </section>
    );
  };
  
  if (document.querySelector('#login-section')){
    ReactDOM.render(<LoginForm/>, document.querySelector('#login-section'));
  }