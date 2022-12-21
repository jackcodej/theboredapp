const RegistrationForm = () => {

// TODO: Add validation to this page
// TODO: Email Validation
// TODO: Password Validation

    return (
    <section>
        <h3 className="mb-4 pb-2 pb-md-0 mb-md-5 px-md-2">Registration</h3>
        <form action="/registration" method="POST" className="px-md-2" >
        <div className="form-outline mb-4">
            <input type="text" id="reg-name" name="name" className="form-control" />
            <label className="form-label">Name</label>
            <input type="text" id="reg-email" name="email" className="form-control" />
            <label className="form-label">Email</label>
            <input type="password" id="reg-password" name="password" className="form-control" />
            <label className="form-label">Password</label>
            <input type="password" id="reg-password-confirm" name="password" className="form-control" />
            <label className="form-label">Confirm Password</label>
            <input type="text" id="reg-zipcode" name="zipcode" className="form-control" />
            <label className="form-label">Zipcode</label>
            <div><input type="submit" value="Register"/></div>
        </div>
        </form>
    </section>
    );
  };
  
  if (document.querySelector('#registration-section')){
    ReactDOM.render(<RegistrationForm/>, document.querySelector('#registration-section'));
  }