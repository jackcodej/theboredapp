const AddActivityForm = () => {

  const [isValid, setIsValid] = React.useState(false);
  const [activity, setActivity] = React.useState("");
  const [price, setPrice] = React.useState("");
  const [link, setLink] = React.useState("");
  
  // Check if activity name is valid
  const activityValidation = () =>{
    // lowercase and uppercase alphabet allowing spaces
    const regex = /^[A-Za-z ]+$/
    return regex.test(activity)
  }

  React.useEffect(() => {
    if (activity !== "" && price !== "" && activityValidation()){
      setIsValid(true);
    } else{
      setIsValid(false);
    }
  })

    return (
    <section>
        <h3 className="pb-md-0">Add an Activity</h3>
        <p>Please fill out the form to add a new activity</p>
        <form action="/add-activity" method="POST" className="px-md-2" >
        <div className="form-outline mb-4">
            <input type="text"
            required
            id="activity" 
            name="activity" 
            value={activity} 
            onChange={(e) => setActivity(e.target.value)}
            className="form-control" />
            <div className="row">
              <div className="col-sm-2"><label className="form-label">Activity</label></div>
              <div className="col-sm-10"><div className="new-activity-form-error" id="activityError"></div></div>
            </div>
            <select class="form-select"  aria-label="Activity type select" name="accessibility">
              <option selected value="">Select an accessibility level</option>
              <option value="few-to-no">Few to no challenges</option>
              <option value="minor">Minor challenges</option>
              <option value="major">Major challenges</option>
            </select>
            <div className="row">
              <div className="col-sm-3"><label className="form-label">Accessibility</label></div>
              <div className="col-sm-10"><div className="new-activity-form-error" id="accessibilityError"></div></div>
            </div>
            <select class="form-select"  aria-label="Activity type select" name="a_type">
              <option selected value="">Select the activity type</option>
              <option value="diy">Do it yourself (diy)</option>
              <option value="cooking">Cooking</option>
              <option value="charity">Charity</option>
              <option value="social">Social</option>
              <option value="music">Music</option>
              <option value="recreational">Recreational</option>
              <option value="relaxation">Relaxation</option>
              <option value="education">Education</option>
              <option value="busywork">Busywork</option>
            </select>
            <div className="row">
              <div className="col-sm-3"><label className="form-label">Type</label></div>
              <div className="col-sm-10"><div className="new-activity-form-error" id="atypeError"></div></div>
            </div>
            <select class="form-select"  aria-label="Activity type select" name="participants">
            <option selected value="">Select number of participants</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
          </select>
            <div className="row">
              <div className="col-sm-3"><label className="form-label">Participants</label></div>
              <div className="col-sm-10"><div className="new-activity-form-error" id="participantsError"></div></div>
            </div>
            <input type="number"
            required
            id="price" 
            name="price" 
            value={price} 
            onChange={(e) => setPrice(e.target.value)}
            className="form-control" />
            <div className="row">
              <div className="col-sm-3"><label className="form-label">Price</label></div>
              <div className="col-sm-10"><div className="new-activity-form-error" id="priceError"></div></div>
            </div>
            <input type="text"
            required
            id="link" 
            name="link" 
            value={link} 
            onChange={(e) => setLink(e.target.value)}
            className="form-control" />
            <div className="row">
              <div className="col-sm-3"><label className="form-label">Link</label></div>
              <div className="col-sm-10"><div className="new-activity-form-error" id="linkError"></div></div>
            </div>
            <div><input className="btn btn-primary" type="submit" value="Add Activity" disabled={!isValid}/></div>
        </div>
        </form>
    </section>
    );
  };
  
  if (document.querySelector('#add-activity')){
    ReactDOM.render(<AddActivityForm/>, document.querySelector('#add-activity'));
  }