<h1>Best Flight Deals</h1>
Get the best prices for flights to all destinations you provide.<br>
Obiora's Flight Club helps you get the best flight deals available.<br>
Send a list of destinations you would like to visit, the app searches the flight API for the best offers.<br>
Keeps a local database to ensure you always have the best deals ever.

<h2>Requirements</h2>
<ul>
  <li>Python 3.8 or higher.</li>
  <li>Create a GoFlightLabs Account (https://app.goflightlabs.com) & get the ICAO Codes for destinations through their API.</li>
  <li>Create a Tequila account (https://tequila.kiwi.com) to get the IATA Code for the desitination cities through their API as well as perform flight price searches.</li>
  <li>Create a new Google Sheets Document.</li>
  <li>Create a Sheety Account (https://dashboard.sheety.co/) to interface with Google Sheets API.</li>
</ul>
<hr>
<h3>What to do</h3>
<ol>
  <li>Fork this Git and clone to your local PC.</li>
  <li>Add an extra sheet so that you have "Sheet1" and "Sheet2" in the Google Sheets Document.</li>
  <li>Save the Google Sheets Filename as Flight Costs; rename "Sheet1" as "costs" and "Sheet2" as "users".</li>
  <li>Copy the url of the Google Sheets Document.</li>
  <li>Login to your Sheety Account and paste the url copied above to enable Sheety access the Google Sheets file.</li>
  <li>Select the options to access Sheety using requests "post" and "put" methods.</li>
  <li>Set your Bearer Authentication token to access the Sheety API.</li>
  <li>Add these information to your environment variables.</li>
  <ul>
    <li>TEQUILA_ENDPOINT=apiForTequilaToGetIataCode</li>
    <li>TEQUILA_TOKEN=authTokenToAccessTequila</li>
    <li>GOFLIGHTLABS_ENDPOINT=apiForGoFlightLabsToGetIcaoCodes</li>
    <li>GOFLIGHTLABS_KEY=authTokenToAccessGoFlightLabs</li>
    <li>FLIGHTSEARCH_ENDPOINT=apiForTequilaToPerformFlightSearches</li>
    <li>RETURN_TICKET=authTokenToAccessFlightSearches</li>
    <li>SHEETY_ENDPOINT=accessSheetyApiToUpdateFlightDetailsAndPricesOnGoogleSheets</li>
    <li>SHEETY_USER_ENDPOINT=accessSheetyApiToUpdateUserDetailsOnGoogleSheets</li>
    <li>SHEETY_AUTH=authTokenToAccessSheetyAPI</li>
    <li>MY_EMAIL=yourEmail</li>
    <li>EMAIL_PASSWORD=yourPassword</li>
  </ul>
  <li>Type 'New' or 'Search' to either register a new user or search for best flight prices.</li>
  <li>If your selection is "New":</li>
  <ul>
    <li>Input first name of new user</li>
    <li>Input last name of new user</li>
    <li>Input the new user's email</li>
    <li>Type the email again for confirmation</li>
    <li>Input the <strong>number</strong> of destinations the user would like to obtain cheaper flight price updates</li>
    <li>Input each of the cities as indicated above.</li>
    <li>That's all you need to do for now.</li>
  </ul>
  <li>However, if you run the code and select "Search":</li>
  <ul>
    <li>You'll definitely get an email if there's a cheaper flight prices.</li>
  </ul>
</ol>
<hr>
<h3>Results</h3>
<img src="https://user-images.githubusercontent.com/30503852/203136992-c9353579-3e7e-4f72-a791-4958be5e07b9.jpg" alt="resultFlightPrices.jpg">
<img src="https://user-images.githubusercontent.com/30503852/203137226-5e7a3856-4a2b-440d-8fdd-787969487dfd.jpg" alt="resultBestDealsCode.jpg">
<img src="https://user-images.githubusercontent.com/30503852/203137560-c013efbb-f3b0-4aab-91cf-1366dbedfb24.jpg" alt="resultUsers.jpg">
<hr>
<h3>Bugs</h3>
<p>None as at the time of this documentation. 😉</p>


