CREATE DATABASE covid_portfolio_project;
USE covid_portfolio_project;

# Creating the 2 tables with appropriate data types, so we don't run into type errors like the original video
CREATE TABLE covid_deaths (
	unknown_col INT,
    iso_code VARCHAR(10),
    continent VARCHAR(100),
    location VARCHAR(100),
    date DATE,
    population BIGINT,
    total_cases INT,
    new_cases INT,
    new_cases_smoothed INT,
    total_deaths INT,
    new_deaths INT,
    new_deaths_smoothed FLOAT,
    total_cases_per_million INT,
    new_cases_per_million FLOAT,
    new_cases_smoothed_per_million FLOAT,
    total_deaths_per_million FLOAT,
    new_deaths_per_million FLOAT,
    new_deaths_smoothed_per_million FLOAT,
    reproduction_rate FLOAT,
    icu_patients INT,
    icu_patients_per_million FLOAT,
    hosp_patients INT,
    hosp_patients_per_million FLOAT,
    weekly_icu_admissions INT,
    weekly_icu_admissions_per_million FLOAT,
    weekly_hosp_admissions INT,
    weekly_hosp_admissions_per_million FLOAT
    );
    
CREATE TABLE covid_vacc (
    unknown_col INT,
    iso_code VARCHAR(10),
    continent VARCHAR(100),
    location VARCHAR(100),
    date DATE,
    total_tests BIGINT,
    new_tests INT,
    total_tests_per_thousand FLOAT,
    new_tests_per_thousand FLOAT,
    new_tests_smoothed INT,
    new_tests_smoothed_per_thousand FLOAT,
    positive_rate FLOAT,
    tests_per_case FLOAT,
    tests_units VARCHAR(15),
    total_vaccinations BIGINT,
    people_vaccinated BIGINT,
    people_fully_vaccinated BIGINT,
    total_boosters BIGINT,
    new_vaccinations INT,
    new_vaccinations_smoothed INT,
    total_vaccinations_per_hundred FLOAT,
    people_vaccinated_per_hundred FLOAT,
    people_fully_vaccinated_per_hundred FLOAT,
    total_boosters_per_hundred FLOAT,
    new_vaccinations_smoothed_per_million INT,
    new_people_vaccinated_smoothed INT,
    new_people_vaccinated_smoothed_per_hundred FLOAT,
    stringency_index FLOAT,
    population_density FLOAT,
    median_age FLOAT,
    aged_65_older FLOAT,
    aged_70_older FLOAT,
    gdp_per_capita FLOAT,
    extreme_poverty FLOAT,
    cardiovasc_death_rate FLOAT,
    diabetes_prevalence FLOAT,
	female_smokers FLOAT,
    male_smokers FLOAT,
    handwashing_facilities FLOAT,
    hospital_beds_per_thousand FLOAT,
    life_expectancy FLOAT,
    human_development_index FLOAT,
    excess_mortality_cumulative_absolute FLOAT,
    excess_mortality_cumulative FLOAT,
    excess_mortality FLOAT,
    excess_mortality_cumulative_per_million FLOAT
);

# Filling the covid deaths table
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/covid_deaths.csv' INTO TABLE covid_deaths
FIELDS TERMINATED BY ','
IGNORE 1 LINES;

# Confirming table with a midsection of the rows (early & late rows contain high number of NULL values)
# DESC covid_deaths;
#SELECT * FROM covid_deaths LIMIT 350000, 351000;

# Filling the vaccinations table
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/covid_vacc.csv' INTO TABLE covid_vacc
FIELDS TERMINATED BY ','
IGNORE 1 LINES;

# Confirming table with a midsection of the rows (early & late rows contain high number of NULL values)
# DESC covid_vacc;
# SELECT * FROM covid_vacc LIMIT 350000, 351000;

# Select Data that we are going to use

SELECT location, date, total_cases, new_cases, total_deaths, population
FROM covid_deaths
WHERE continent != '0'
ORDER BY location, date;

# Looking at Total Cases vs Total Deaths
# Shows likelihood of dying if you contracted covid in the US
SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as deaths_percentage
FROM covid_deaths
WHERE location like '%states%'
ORDER BY location, date;

# Shows likelihood of dying if you contracted covid in Japan
SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as deaths_percentage
FROM covid_deaths
WHERE location = 'Japan'
ORDER BY location, date;

# Looking at Total Cases vs Population
# Shows what percentage of US population got Covid
SELECT location, date, total_cases, population, (total_cases/population)*100 as infected_pop_percentage
FROM covid_deaths
WHERE location like '%states%'
ORDER BY location, date;

# Shows what percentage of Japanese population got Covid
SELECT location, date, total_cases, population, (total_cases/population)*100 as infected_pop_percentage
FROM covid_deaths
WHERE location = 'Japan'
ORDER BY location, date;

# Looking at countries with highest infection rate compared to population
SELECT location, 
		population, 
        MAX(total_cases) as max_infection_count, 
        MAX((total_cases/population))*100 as infected_pop_percentage
FROM covid_deaths
WHERE continent != '0'
GROUP BY location, population
ORDER BY infected_pop_percentage DESC;

# Looking at countries with highest total death count
SELECT location, 
        MAX(total_deaths) as max_death_count
FROM covid_deaths
WHERE continent != '0'
GROUP BY location
ORDER BY max_death_count DESC;

# Total death count by continent (correct way)
SELECT location,
        MAX(total_deaths) as max_death_count
FROM covid_deaths
WHERE continent = '0'
GROUP BY location
ORDER BY max_death_count DESC;

# Total death count by continent (wrong way)
SELECT continent,
        MAX(total_deaths) as max_death_count
FROM covid_deaths
WHERE continent != '0'
GROUP BY continent
ORDER BY max_death_count DESC;

# Global numbers
SELECT 
	SUM(new_cases) as total_new_cases, 
	SUM(new_deaths) as total_new_deaths, 
    SUM(new_deaths)/SUM(new_cases)*100 as death_percentage
FROM covid_deaths
WHERE continent != '0';

# Total Population vs Vaccination
# Use CTE
With pop_vs_vac (continent, location, date, population, new_vaccination, rolling_vacc_total)
AS
(
SELECT 
	dea.continent, 
    dea.location, 
    dea.date, 
    dea.population, 
    vac.new_vaccinations,
    SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as rolling_vacc_total
FROM covid_deaths dea 
JOIN covid_vacc vac 
	ON dea.location = vac.location
    AND dea.date = vac.date
WHERE dea.continent != '0'
# ORDER BY 2, 3
)
SELECT *, (rolling_vacc_total/population)*100 as rolling_population_percentage
FROM pop_vs_vac
;

# Use TEMP table instead of CTE

DROP TABLE IF EXISTS percent_population_vaccinated;
CREATE TABLE percent_population_vaccinated (
    continent VARCHAR(100),
    location VARCHAR(100),
    date DATE,
    population BIGINT,
    new_vaccinations INT,
    rolling_vacc_total BIGINT
    );

INSERT INTO percent_population_vaccinated
SELECT 
	dea.continent, 
    dea.location, 
    dea.date, 
    dea.population, 
    vac.new_vaccinations,
    SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as rolling_vacc_total
FROM covid_deaths dea 
JOIN covid_vacc vac 
	ON dea.location = vac.location
    AND dea.date = vac.date
WHERE dea.continent != '0'
;

SELECT *, (rolling_vacc_total/population)*100 as rolling_population_percentage
FROM percent_population_vaccinated
ORDER BY location, date;

# Creating View to Store Data For Visualizations
CREATE VIEW percent_poppercent_pop_vaccinatedcontinent_vaccinated as
SELECT 
	dea.continent, 
    dea.location, 
    dea.date, 
    dea.population, 
    vac.new_vaccinations,
    SUM(vac.new_vaccinations) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as rolling_vacc_total
FROM covid_deaths dea 
JOIN covid_vacc vac 
	ON dea.location = vac.location
    AND dea.date = vac.date
WHERE dea.continent != '0'
;