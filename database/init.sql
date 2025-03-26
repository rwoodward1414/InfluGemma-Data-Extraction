
CREATE TABLE countries (
    CountryID int NOT NULL,
    CountryName varchar(255) NOT NULL,
    Region varchar(255) NOT NULL,
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

INSERT INTO countries (CountryID, CountryName, Region)
VALUES
(1, 'Australia', 'South'),
(2, 'USA', 'North');

INSERT INTO states (StateID, StateName, CountryID)
VALUES
(1, 'ACT', 1),
(2, 'NSW', 1),
(3, 'NT', 1),
(4, 'QLD', 1),
(5, 'SA', 1),
(6, 'TAS', 1),
(7, 'VIC', 1),
(8, 'WA', 1);