const RegistrationForm = () => {

  // TODO: Add error msgs/tooltips to show users requirements and which are incomplete (after they start)

  // Create controlled components so I can validate information before allowing users to 'register'
  const [isValid, setIsValid] = React.useState(false);
  const [name, setName] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [confirmPassword, setConfirmPassword] = React.useState("");
  const [zipcode, setZipcode] = React.useState("");

  // Check if name is valid
  const nameValidation = () =>{
    // lowercase and uppercase alphabet allowing spaces
    const regex = /^[A-Za-z ]+$/
    return regex.test(name)
  }

  // Check if email is valid
  const emailValidation = () =>{
    // alphanumeric including '-' and '_' separated by an '@' sign followed by the previous condition then separated with a period ending with 2-5 alpha chars
    const regex = /^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/;
    return regex.test(email)
  }

  // Check if password meets minimum character requirement
  const strongPassword = () =>{
    // 8 or more of any characters
    const regex = /.{8,}/;
    return regex.test(password)
  }
  
  // Check if passwords match
  const passwordsMatch = () =>{
    if (password === confirmPassword){
      return true
    }
    return false
  }

  // Check if zipcode is valid
  const zipcodeValidation = () =>{
    // regex for valid United States zipcodes
    const regex = /(^\d{5}$)|(^\d{9}$)|(^\d{5}-\d{4}$)/;
    return regex.test(zipcode)
  }

  // useEffect will listen to changes in variables in the defined array and run this code when is sees changes
  React.useEffect(() =>{
    emailValidation();
    // Check if any field is empty or invalid
    if (name === "" || 
    email === "" || 
    password === "" || 
    confirmPassword === "" || 
    zipcode === "" || 
    !nameValidation() || 
    !emailValidation() ||
    !strongPassword() || 
    !passwordsMatch() ||
    !zipcodeValidation()
    ){
      setIsValid(false);
      // add individual ELIFS or just check each field with its own conditional for empty / valid using regex
    } else{
      setIsValid(true);
    }

  },[isValid, name, email, password, confirmPassword, zipcode])

    return (
    <section>
        <h3 className="mb-4 pb-2 pb-md-0 mb-md-5 px-md-2">Registration</h3>
        <form action="/registration" method="POST" className="px-md-2" >
        <div className="form-outline mb-4">
            <input type="text" 
            id="reg-name" 
            name="name" 
            value={name} 
            onChange={(e) => setName(e.target.value)}
            className="form-control" />
          <label className="form-label">Name</label>
            <input type="text" 
            id="reg-email" 
            name="email"
            value={email} 
            onChange={(e) => setEmail(e.target.value)}
            className="form-control" />
          <label className="form-label">Email</label>
            <input type="password" 
            id="reg-password" 
            name="password"
            value={password} 
            onChange={(e) => setPassword(e.target.value)}
            className="form-control" />
          <label className="form-label">Password</label>
            <input type="password" 
            id="reg-password-confirm" 
            name="password-confirm" 
            value={confirmPassword} 
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="form-control" />
          <label className="form-label">Confirm Password</label>
            <input type="text" 
            id="reg-zipcode" 
            name="zipcode" 
            value={zipcode} 
            onChange={(e) => setZipcode(e.target.value)}
            className="form-control" />
          <label className="form-label">Zipcode</label>
            <div><input className="btn btn-primary" type="submit" value="Register" disabled={!isValid}/></div>
        </div>
        </form>
    </section>
    );
  };
  
  if (document.querySelector('#registration-section')){
    ReactDOM.render(<RegistrationForm/>, document.querySelector('#registration-section'));
  }