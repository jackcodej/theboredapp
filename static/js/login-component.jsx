const LoginForm = () => {

  // Make email and password controlled state components to match registration-component
  // No need to add true validation here since server.py will deny all bad inputs
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [disable, setDisable] = React.useState(true);

  React.useEffect(() =>{
    if (email === "" || password === ""){
      setDisable(true)
    }
    else{
      setDisable(false)
    }
  },[email, password]);

    return (
    <section>
        <h3 className="mb-4 pb-2 pb-md-0 mb-md-5 px-md-2">Log in</h3>
        <form action="/login" method="POST" className="px-md-2" >
        <div className="form-outline mb-4">
            <input type="text" 
            id="login-email" 
            name="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)}
            className="form-control" />
            <label className="form-label">Email</label>
            <input type="password" 
            id="login-password" 
            name="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)}
            className="form-control" />
            <label className="form-label">Password</label>
            <div><input className="btn btn-primary" disabled={disable} type="submit" value="Login"/></div>
        </div>
        </form>
    </section>
    );
  };
  
  if (document.querySelector('#login-section')){
    ReactDOM.render(<LoginForm/>, document.querySelector('#login-section'));
  }