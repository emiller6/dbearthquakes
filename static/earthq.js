"use strict"

const ce = React.createElement;
//const csrfToken = document.getElementById("csrfToken").value;
const sendimpact = document.getElementById("sendimpact").value;
const getRecentHome = document.getElementById("recentshome").value;
const findbydate = document.getElementById("searchbydate").value;
const findbyloc = document.getElementById("searchbyloc").value;
const findbyid = document.getElementById("searchbyid").value;
const updatebyid = document.getElementById("updatebyid").value;
const deletebyid = document.getElementById("deletebyid").value;

class EarthquakesMainComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {page: "H", eq_id: ""};
    this.handlePageChange = this.handlePageChange.bind(this);
    this.handleDetails = this.handleDetails.bind(this);
  }

  handlePageChange(page){
    this.setState({page});
  }

  handleDetails(page, eq_id){
    this.setState({eq_id: eq_id}, () => {
          console.log(this.state.eq_id);
          this.setState({page});
    });
  }

  render() {
    switch(this.state.page) {
      case "H": return ce('div', null, ce(HeaderComponent, {changePage: this.handlePageChange}), ce(HomeComponent, {changePage: this.handleDetails}));
      case "I": return ce('div', null, ce(HeaderComponent, {changePage: this.handlePageChange}), ce(ImpactComponent));
      case "F": return ce('div', null, ce(HeaderComponent, {changePage: this.handlePageChange}), ce(FindQuakeComponent, {changePage: this.handleDetails}));
      case "D": return ce('div', null, ce(HeaderComponent, {changePage: this.handlePageChange}), ce(DetailedViewComponent, {eq_id: this.state.eq_id}));
      //case "L": return ce('div', null, ce(HeaderComponent, {changePage: this.handlePageChange}), ce(LabComponent));
      case _: return ce('p',null,'FAIL');
    }
  }
}

class HeaderComponent extends React.Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e, str) {
    this.props.changePage(str);
  }

  render() {
    return ce('div', 'null',
        ce('nav',{className: "navbar_home"},
          ce('button', {onClick: e => this.handleChange(e,"H")}, 'Home'),
          ce('button', {onClick: e => this.handleChange(e,"F")}, 'Find an Earthquake'),
          ce('button', {onClick: e => this.handleChange(e,"I")}, 'Submit an Impact Report'),
          //ce('button', {onClick: e => this.handleChange(e,"L")}, 'Laboratory View')
        )
    );
  }
}

class HomeComponent extends React.Component {
  constructor(props) {
    super(props);
    this.openDetails = this.openDetails.bind(this);
    this.state = {eq_id: "", rqs: [{index: 1, epicenter_longitude: 20, epicenter_latitude: 20, datetime: "10/7/21 10:50AM", magnitude: 3, depth: 2.2},{index: 2, epicenter_longitude: 10, epicenter_latitude: 20, datetime: "10/7/21 10:50AM", magnitude: 3, depth: 2.2}]}
  }

  openDetails(key, str) {
    console.log(key);
    console.log(key.index);
    this.props.changePage(str, key.index);
  }

  componentDidMount() {
    console.log(1);
    fetch(getRecentHome, {
      method: 'GET',
      headers: {'Content-Type': 'application/json'},
    }).then(res => res.json()).then(data => {
      this.setState({rqs: data['data']})});
    console.log(2);
//    var newData = this.state.rqs.concat([this.state.rqs]);
//    this.setState({rqs: newData});
  }

  render() {
    console.log(this.state.rqs);
    return ce('div',{className: "main_page"},
      ce('div', {className: "descrip_box"},
        ce('h2',null,'Welcome to the Earthquake Database!')
      ),
      ce('div', {className: "recent_quakes"},
        ce('h2', null, 'Recent Earthquakes'),
        ce('table', {className: "recentq"},
          ce('tbody',null ,
            ce('tr',null,
              ce('th', {key: 0}, "Date/Time"),
              ce('th', {key: 1}, "Longitude of Epicenter"),
              ce('th', {key: 2}, "Latitude of Epicenter"),
              ce('th', {key: 3}, "Magnitude"),
              ce('th', {key: 4}, "Depth")
            ),
            this.state.rqs.map((quake) => {
              return (
                ce('tr',{key:quake.index, onClick: () => this.openDetails(quake,'D')},
                  ce('td', null, quake.datetime),
                  ce('td', null, quake.epicenter_longitude),
                  ce('td', null, quake.epicenter_latitude),
                  ce('td', null, quake.magnitude),
                  ce('td', null, quake.depth)
                )
              )
            })
          )
        )
      )
    );
  }
}


class ImpactComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {city: "", state_loc: "", eq_date: "", rating: "", comments: "", error: ""}
  }

  typingHandler(e) {
    console.log(e.target.value);
    this.setState({[e.target['id']]: e.target.value});
  }

  addImpact(e) {
    const city = this.state.city;
    const st = this.state.state_loc;
    const eq_date = this.state.eq_date;
    const rating = this.state.rating;
    const comments = this.state.comments;
    fetch(sendimpact, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({"city": city, "state": st, "date": eq_date, "rating": rating, "comments": comments})
    }).then(res => res.json()).then(data => {
      if(data) {
        this.setState({city: ""});
        this.setState({state_loc: ""});
        this.setState({eq_date: ""});
        this.setState({rating: ""});
        this.setState({comments: ""});
      } else {
        this.setState({error: "SUBMISSION FAILED, PLEASE TRY AGAIN"});
      }
    });
  }

  render() {
    return ce('div', {className: "impact_form"},
      ce('h2',null,'Tell Us What You Experienced'),
      'City: ', ce('input',{type: "text", id: "city", value: this.state.city, onChange: e => this.typingHandler(e)}), ce('br'),
      'State: ', ce('input',{type: "text", id: "state_loc", value: this.state.state_loc, onChange: e => this.typingHandler(e)}), ce('br'),
      'Date: ', ce('input',{type: "datetime-local", id: "eq_date", value: this.state.eq_date, onChange: e => this.typingHandler(e)}), ce('br'),
      'Rate the Effects (1 (no damage) to 5 (heavy damage)): ',
      ce('input',{type: "number", min: 1, max: 5, id: "rating", value: this.state.rating, onChange: e => this.typingHandler(e)}),
      ce('br'), 'Description: ', ce('input',{type: "text", id: "comments", value: this.state.comments, onChange: e => this.typingHandler(e)}),
      ce('br'), ce('br'), ce('button', {onClick: e => this.addImpact(e)}, 'Submit'),
      ce('span',{id: "error-submit"}, this.state.error)
    );
  }
}

class FindQuakeComponent extends React.Component {
  constructor(props) {
    super(props);
    this.openDetails = this.openDetails.bind(this);
    this.state = {eq_id: "", error: "", date: "", tablename: "Recent Earthquakes", city: "", st: "", rqs: [{index: 1, epicenter_longitude: 10, epicenter_latitude: 20, datetime: "10/7/21 10:50AM", magnitude: 3, depth: 2.2}]}
  }

  typingHandler(e) {
    this.setState({[e.target['id']]: e.target.value});
  }

  findQuakes(e) {
    if(this.state.date == ""){
      this.findQuakesByLocation(e);
    } else {
      this.findQuakesByDate(e);
    }
  }

  findQuakesByLocation(e) {
    this.setState({tablename: 'Search Results'});
    fetch(findbyloc, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({city: this.state.city, state: this.state.st})
    }).then(res => res.json()).then(data => {
      if(data) {
        this.setState({rqs: data['data']});
      } else {
        this.setState({error: "No results found."});
        this.setState({rqs: []});
      }
    });
  }

  findQuakesByDate(e) {
    this.setState({tablename: 'Search Results'});
    fetch(findbydate, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({datetime: this.state.date})
    }).then(res => res.json()).then(data => {
      if(data) {
        this.setState({rqs: data['data']});
      } else {
        this.setState({error: "No results found."});
        this.setState({rqs: []});
      }
    });
  }

  componentDidMount() {
    fetch(getRecentHome).then(res => res.json()).then(data => this.setState({rqs: data['data']}));

  }

  openDetails(key, str) {
    console.log(key);
    console.log(key.index);
    this.props.changePage(str, key.index);
  }

  render() {
    return ce('div', {className: "findquake"},
      ce('h2',null,'Find an Earthquake'),
      //Search by date
      'Search by Date: ',
      ce('input',{type: "date", id: "date", value: this.state.date, onChange: e => this.typingHandler(e)}),
      //Search by location
      ' or City: ',
      ce('input',{type: "text", id: "city", value: this.state.city, onChange: e => this.typingHandler(e)}),
      ' and State: ',
      ce('input',{type: "text", id: "st", value: this.state.st, onChange: e => this.typingHandler(e)}), '\t\t',
      ce('button', {onClick: e => this.findQuakes(e)}, 'Search'),
      //Table of recent earthquakes
      ce('h2',null,this.state.tablename),
      ce('span',{id: "search_error"},this.state.error),
      ce('table', {className: "recentq"},
        ce('tbody',null ,
          ce('tr',null,
            ce('th', {key: 0}, "Date/Time"),
            ce('th', {key: 1}, "Longitude of Epicenter"),
            ce('th', {key: 2}, "Latitude of Epicenter"),
            ce('th', {key: 3}, "Magnitude"),
            ce('th', {key: 4}, "Depth")
          ),
          this.state.rqs.map((quake) => {
            return (
              ce('tr',{key:quake.index, onClick: () => this.openDetails(quake,'D')},
                ce('td', null, quake.datetime),
                ce('td', null, quake.epicenter_longitude),
                ce('td', null, quake.epicenter_latitude),
                ce('td', null, quake.magnitude),
                ce('td', null, quake.depth)
              )
            )
          })
        )
      )
    );
  }
}

class DetailedViewComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {error: "", id_code: "", valid: false, rqs: [], eq_id: props.eq_id, datetime: "2012", mag: "10", depth: "3", city: "Los Angeles", st: "CA", predicted: "4.2", avgrating: "3.7", comments: []};
  }


  typingHandler(e) {
    this.setState({[e.target['id']]: e.target.value});
  }

  componentDidMount() {
    this.setState({eq_id: this.props.eq_id}, () => {
          console.log(this.state.eq_id);
    });
    fetch(findbyid, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({eq_id: this.state.eq_id})
    }).then(res => res.json()).then(data => {
      if(data) {
        this.setState({rqs: data['data']}, () => {
          console.log(this.state.rqs);
          this.setState({valid: false});
          this.setState({eq_id: this.state.rqs.index});
          this.setState({datetime: this.state.rqs.datetime});
          this.setState({mag: this.state.rqs.magnitude});
          this.setState({depth: this.state.rqs.depth});
          this.setState({city: this.state.rqs.city});
          this.setState({st: this.state.rqs.state});
          this.setState({predicted: this.state.rqs.pred_impact});
          this.setState({avgrating: this.state.rqs.cur_impact});
          this.setState({comments: this.state.rqs.comments});
        });

      } else {
        this.setState({error: "No results found."});
        this.setState({rqs: []});
      }
    });
  }

  allowEdits(e){
    console.log(this.state.id_code);
    if(this.state.id_code == "valid123"){
      console.log("here");
      this.setState({valid: true});
    }
  }

  update(e){
    fetch(updatebyid, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({eq_id: this.state.eq_id, datetime: this.state.datetime, mag: this.state.mag, depth: this.state.depth})
    }).then(res => res.json()).then(data => {
      if(data) {
        this.setState({valid: false});
      } else {
        this.setState({error: "Update failed."});
      }
    });
  }

  delete(e){
    fetch(deletebyid, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({eq_id: this.state.eq_id})
    }).then(res => res.json()).then(data => {
      if(data) {
        this.setState({valid: false});
        this.setState({rqs: []});
        this.setState({eq_id: ""});
        this.setState({datetime: ""});
        this.setState({mag: ""});
        this.setState({depth: ""});
        this.setState({city: ""});
        this.setState({st: ""});
        this.setState({predicted: ""});
        this.setState({avgrating: ""});
        this.setState({comments: []});
      } else {
        this.setState({error: "Cannot delete."});
      }
    });
  }

  render() {
    if(this.state.valid){
      return ce('div', {className: "details"},
      ce('h2', null, 'Earthquake Details'),
      ce('h2', null, this.state.error),
      ce('h3', null, 'Date and Time of Event: '), ce('input', {type:"text", id: "datetime", value: this.state.datetime,  onChange: e => this.typingHandler(e)}),
      ce('h3', null, 'Magnitude:'), ce('input', {type: "text", id: "mag", value: this.state.mag, onChange: e => this.typingHandler(e)}),
      ce('h3', null, 'Depth:'), ce('input', {type: "text", id: "depth", value: this.state.depth, onChange: e => this.typingHandler(e)}),
      ce('h3', null, 'Location of Epicenter:'), ce('p', null, this.state.city, ', ', this.state.st),
      ce('h3', null, 'Predicted Impact:'), ce('p', null, this.state.predicted),
      ce('h3', null, 'Current Average of Ratings Impacts:'), ce('p', null, this.state.avgrating),
      ce('table', {className: "impact_comments"},
        ce('tbody',null ,
          ce('tr',null,
            ce('th', {key: 0}, "Impact Reviews"),
          ),
          this.state.comments.map((cmt, index) => {
            return (
              ce('tr',{key:index},
                ce('td', null, cmt)
              )
            )
          })
        )
      ),
      ce('button', {onClick: e => this.delete(e)}, 'Delete Record'),
      ce('button', {onClick: e => this.update(e)}, 'Update Record')
      );
    } else {
      return ce('div', {className: "details"},
      ce('h2', null, 'Earthquake Details'),
      ce('h2', null, this.state.error),
      ce('h3', null, 'Date and Time of Event: '), ce('p', null, this.state.datetime),
      ce('h3', null, 'Magnitude:'), ce('p', null, this.state.mag),
      ce('h3', null, 'Depth:'), ce('p', null, this.state.depth),
      ce('h3', null, 'Location of Epicenter:'), ce('p', null, this.state.city, ', ', this.state.st),
      ce('h3', null, 'Predicted Impact:'), ce('p', null, this.state.predicted),
      ce('h3', null, 'Current Average of Ratings Impacts:'), ce('p', null, this.state.avgrating),
      ce('table', {className: "impact_comments"},
        ce('tbody',null ,
          ce('tr',null,
            ce('th', {key: 0}, "Impact Reviews"),
          ),
          this.state.comments.map((cmt, index) => {
            return (
              ce('tr',{key:index},
                ce('td', null, cmt)
              )
            )
          })
        )
      ),
      ce('div', {className: "LabEdits"},
        ce('h2', null, 'Please enter your verification code to edit or delete earthquake data:'),
        ce('input', {type: "text", id: "id_code", value: this.state.id_code, onChange: e => this.typingHandler(e)}),
        ce('button',{onClick: e => this.allowEdits(e)},'Submit'))
      );
    }
  }
}

ReactDOM.render(
  React.createElement(EarthquakesMainComponent, null, null),
  document.getElementById('main-root')
);
