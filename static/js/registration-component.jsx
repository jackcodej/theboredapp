const RegistrationForm = () => {

  // TODO: Convert validation to onblur instead of useEffect for feedback to users

  // Create controlled components so I can validate information before allowing users to 'register'
  const [isValid, setIsValid] = React.useState(false);
  const [name, setName] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [confirmPassword, setConfirmPassword] = React.useState("");
  const [zipcode, setZipcode] = React.useState("");
  // Error messages
  const [nameError, setNameError] = React.useState("");
  const [emailError, setEmailError] = React.useState("");
  const [passwordError, setPasswordError] = React.useState("");
  const [confirmPasswordError, setConfirmPasswordError] = React.useState("");
  const [zipcodeError, setZipcodeError] = React.useState("");
  // Error message timeout
  const [delayInSec] = React.useState(5);

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
    // Error handling for name
    if (name !== "" && !nameValidation()){
      setNameError("Name is not valid please only use alphabetic characters, spaces are allowed");
    } else{
      setNameError("");
    }

    if (email !== "" && !emailValidation()){
      setTimeout(() => {
        setEmailError("Email is not valid");
      }, delayInSec * 1000);
    } else{
      setEmailError("");
    }
    if (password !== "" && !strongPassword()){
      setTimeout(() => {
        setPasswordError("Password is not long enough, minimum of 8 characters, no spaces");
      }, delayInSec * 1000);
    } else{
      setPasswordError("");
    }

    if (passwordError === "" && confirmPassword !== "" && !passwordsMatch()){
      setTimeout(() => {
        setConfirmPasswordError("Passwords do not match");
      }, delayInSec * 1000);
    } else{
      setConfirmPasswordError("");
    }

    if (zipcode !== "" && !zipcodeValidation()){
      setTimeout(() => {
        setZipcodeError("Zipcode is not a valid U.S. zipcode");
      }, delayInSec * 1000);
    } else{
      setZipcodeError("");
    }

      setEmailError("");
      setPasswordError("");
      setConfirmPasswordError("");
      setZipcodeError("");

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
    } else{
      setIsValid(true);
    }

  },[isValid, name, email, password, confirmPassword, zipcode])

    return (
    <section>
        <h3 className="pb-md-0">Registration</h3>
        <p>Please fill out the form to register</p>
        <form action="/registration" method="POST" className="px-md-2" >
        <div className="form-outline mb-4">
            <input type="text"
            required
            id="reg-name" 
            name="name" 
            value={name} 
            onChange={(e) => setName(e.target.value)}
            className="form-control" />
            <div className="row">
              <div className="col-sm-2"><label className="form-label">Name</label></div>
              <div className="col-sm-10"><div className="reg-form-error" id="nameError">{nameError}</div></div>
            </div>
            <input type="text" 
            id="reg-email" 
            name="email"
            value={email} 
            onChange={(e) => setEmail(e.target.value)}
            className="form-control" />
            <div className="row">
              <div className="col-sm-2"><label className="form-label">Email</label></div>
             {!emailValidation() && (<div className="col-sm-10"><div className="reg-form-error" id="emailError">{emailError}</div></div>)}
            </div>
            <input type="password" 
            id="reg-password" 
            name="password"
            value={password} 
            onChange={(e) => setPassword(e.target.value)}
            className="form-control" />
            <div className="row">
              <div className="col-sm-2"><label className="form-label">Password</label></div>
              {!strongPassword() && (<div className="col-sm-10"><div className="reg-form-error" id="passwordError">{passwordError}</div></div>)}
            </div>
            <input type="password" 
            id="reg-password-confirm" 
            name="password-confirm" 
            value={confirmPassword} 
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="form-control" />
           <div className="row">
              <div className="col-sm-4"><label className="form-label">Confirm Password</label></div>
              {!passwordsMatch() && (<div className="col-sm-8"><div className="reg-form-error" id="confirmPasswordError">{confirmPasswordError}</div></div>)}
            </div>
            <input type="text" 
            id="reg-zipcode" 
            name="zipcode" 
            value={zipcode} 
            onChange={(e) => setZipcode(e.target.value)}
            className="form-control" />
            <div className="row">
              <div className="col-sm-2"><label className="form-label">Zipcode</label></div>
              {!zipcodeValidation() && (<div className="col-sm-10"><div className="reg-form-error" id="zipcodeError">{zipcodeError}</div></div>)}
            </div>
            <div><input className="btn btn-primary" type="submit" value="Register" disabled={!isValid}/></div>
        </div>
        </form>
    </section>
    );
  };
  
  if (document.querySelector('#registration-section')){
    ReactDOM.render(<RegistrationForm/>, document.querySelector('#registration-section'));
  }