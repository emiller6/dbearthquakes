"use strict"

const ce = React.createElement;

class EarthquakesMainComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {page: "H"};
    this.handlePageChange = this.handlePageChange.bind(this);
  }

  handlePageChange(page){
    this.setState({page});
  }

  render() {
    switch(this.state.page) {
      case "H": return ce('div', null, ce(HeaderComponent, {changePage: this.handlePageChange}), ce(HomeComponent, {changePage: this.handlePageChange}));
      case "I": return ce('div', null, ce(HeaderComponent, {changePage: this.handlePageChange}), ce(ImpactComponent));
      case "F": return ce('div', null, ce(HeaderComponent, {changePage: this.handlePageChange}), ce(FindQuakeComponent, {changePage: this.handlePageChange}));
      case "D": return ce('div', null, ce(HeaderComponent, {changePage: this.handlePageChange}), ce(DetailedViewComponent));
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
          ce('button', {onClick: e => this.handleChange(e,"I")}, 'Submit an Impact Report')
          //ce('button', {onClick: e => this.handleChange(e,"L")}, 'Laboratory View')
        )
    );
  }
}

class HomeComponent extends React.Component {
  constructor(props) {
    super(props);
    this.openDetails = this.openDetails.bind(this);
    this.state = {rqs: [{index: 1, epicenter_longitude: 10, epicenter_latitude: 20, datetime: "10/7/21 10:50AM", magnitude: 3, depth: 2.2}]}
  }

  openDetails(e, str) {
    this.props.changePage(str);
  }

  render() {
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
                ce('tr',{key:quake.index, onClick: e => this.openDetails(e,'D')},
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
    this.state = {city: "", state_loc: "", eq_date: "", rating: "", comments: ""}
  }

  typingHandler(e) {
    this.setState({[e.target['id']]: e.target.value});
  }

  addImpact(e) {
    //client.connect();
    //var query = client.query("INSERT ");
    //client.end();
  }

  render() {
    return ce('div', {className: "impact_form"},
      ce('h2',null,'Tell Us What You Experienced'),
      'City: ', ce('input',{type: "text", id: "city", value: this.state.city, onChange: e => this.typingHandler(e)}), ce('br'),
      'State: ', ce('input',{type: "text", id: "state_loc", value: this.state.state_loc, onChange: e => this.typingHandler(e)}), ce('br'),
      'Date: ', ce('input',{type: "datetime-local", id: "eq_date", value: this.state.eq_date, onChange: e => this.typingHandler(e)}), ce('br'),
      ce('br'), 'Rate the Effects: ', ce('br'),
      'No Impact', ce('input',{type: "range", min: 1, max: 5, value: this.state.rating, onChange: e => this.typingHandler(e)}), 'Heavy Damages', ce('br'),
      ce('br'), 'Description: ', ce('input',{type: "text", id: "comments", value: this.state.comments, onChange: e => this.typingHandler(e)}),
      ce('br'), ce('br'), ce('button', {onClick: e => this.addImpact(e)}, 'Submit')
    );
  }
}

class FindQuakeComponent extends React.Component {
  constructor(props) {
    super(props);
    this.openDetails = this.openDetails.bind(this);
    this.state = {date: "", tablename: "Recent Earthquakes", city: "", st: "", rqs: [{index: 1, epicenter_longitude: 10, epicenter_latitude: 20, datetime: "10/7/21 10:50AM", magnitude: 3, depth: 2.2}]}
  }

  typingHandler(e) {
    this.setState({[e.target['id']]: e.target.value});
  }

  findQuakesByLocation(e) {
    this.state.tablename = 'Search Results';
    client.connect();
    //use city table to convert name to lat, long
    //query = client.query("SELECT latitude, longitude FROM City WHERE name = ${city} AND state = ${st}")

    long = 0//find city epicenter_longitude
    lat = 0//find city epicenter_latitude

    //populate table with earthquake data related to search results
    //query = client.query("SELECT * FROM Earthquake WHERE epicenter_longitude<=${long} AND epicenter_longitude>=${long} AND epicenter_latitude<=${lat} AND epicenter_latitude>=${lat}");

    //get results
    //query.on("row", function(row, result){
      //result.addRow(row);
    //});

    //client.end();
  }

  openDetails(e, str) {
    this.props.changePage(str);
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
      ce('button', {onClick: e => this.findQuakesByLocation(e)}, 'Search'),
      //Table of recent earthquakes
      ce('h2',null,this.state.tablename),
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
              ce('tr',{key:quake.index, onClick: e => this.openDetails(e, 'D')},
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
    this.state = {datetime: "2012", mag: "10", depth: "3", city: "Los Angeles", state: "CA", predicted: "4.2", avgrating: "3.7", comments: []};
  }

  componentDidMount() {

  }

  render() {
    return ce('div', {className: "details"},
      ce('h2', null, 'Earthquake Details'),
      ce('h3', null, 'Date and Time of Event: '), ce('p', null, this.state.datetime),
      ce('h3', null, 'Magnitude:'), ce('p', null, this.state.mag),
      ce('h3', null, 'Depth:'), ce('p', null, this.state.depth),
      ce('h3', null, 'Location of Epicenter:'), ce('p', null, this.state.city, ', ', this.state.state),
      ce('h3', null, 'Predicted Impact:'), ce('p', null, this.state.predicted),
      ce('h3', null, 'Current Average of Ratings Impacts:'), ce('p', null, this.state.avgrating),
      ce('h3', null, 'Impact Reviews:')
      //Date/time, magnitude, depth, city, state, predicted impact, ratings average, comments
    )
  }
}

ReactDOM.render(
  React.createElement(EarthquakesMainComponent, null, null),
  document.getElementById('main-root')
);
