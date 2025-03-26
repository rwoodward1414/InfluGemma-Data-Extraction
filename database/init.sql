
CREATE TABLE countries (
    CountryID int NOT NULL,
    CountryName varchar(255) NOT NULL,
    Region ENUM('North', 'South') NOT NULL,
    PRIMARY KEY (CountryID)
);

CREATE TABLE states (
    StateID int NOT NULL,
    StateName varchar(255) NOT NULL,
    CountryID int NOT NULL,
    PRIMARY KEY (StateID),
    FOREIGN KEY (CountryID) REFERENCES countries(CountryID)
);

CREATE TABLE fornight_surv_data (
    StateID int NOT NULL,
    EndDate DATE NOT NULL,
    CaseNumber int NOT NULL,
    FOREIGN KEY (StateID) REFERENCES states(StateID)
);

