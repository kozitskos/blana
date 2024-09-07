// Exporting the function to generate a random celebrity name
export function generateCelebrityName(): string {
    // List of 100 celebrity first names
    const firstNames: string[] = [
        'Scarlett', 'Tom', 'Brad', 'Angelina', 'Jennifer', 'Leonardo', 'Emma', 'Robert', 'Chris', 'Natalie',
        'Johnny', 'Will', 'Sandra', 'Keanu', 'Anne', 'Ryan', 'Nicole', 'Julia', 'Samuel', 'Morgan',
        'Dwayne', 'Matthew', 'Meryl', 'Hugh', 'George', 'Cate', 'Matt', 'Amy', 'Liam', 'Zoe',
        'Christian', 'Chadwick', 'Gwyneth', 'Gal', 'Chris', 'Jake', 'Sophie', 'Daniel', 'Harrison', 'Mark',
        'Viola', 'Margot', 'Henry', 'Zendaya', 'Eddie', 'Michael', 'Tilda', 'Emma', 'Tom', 'Jason',
        'Ryan', 'Megan', 'Adam', 'Zac', 'Joaquin', 'Eva', 'Emily', 'Javier', 'Anne', 'Amy',
        'Salma', 'Ben', 'Heath', 'Chris', 'Jason', 'Jared', 'Charlize', 'Tom', 'Tobey', 'Denzel',
        'Rachel', 'Bryce', 'Idris', 'Kate', 'Orlando', 'Natalie', 'Benedict', 'Kristen', 'Shia', 'Billie',
        'Halle', 'Jude', 'Vin', 'Daisy', 'Reese', 'David', 'Channing', 'Timothée', 'Zoe', 'Scarlett',
        'John', 'Drew', 'Mila', 'Jason', 'Elizabeth', 'Cillian', 'Florence', 'Chris', 'Tom', 'Penélope'
    ];

    // List of 100 family names
    const lastNames: string[] = [
        'Johnson', 'Smith', 'Pitt', 'Jolie', 'Lawrence', 'DiCaprio', 'Watson', 'Downey', 'Evans', 'Portman',
        'Depp', 'Smith', 'Bullock', 'Reeves', 'Hathaway', 'Gosling', 'Kidman', 'Roberts', 'Jackson', 'Freeman',
        'Johnson', 'McConaughey', 'Streep', 'Jackman', 'Clooney', 'Blanchett', 'Damon', 'Adams', 'Hemsworth', 'Saldana',
        'Bale', 'Boseman', 'Paltrow', 'Gadot', 'Pratt', 'Gyllenhaal', 'Turner', 'Craig', 'Ford', 'Ruffalo',
        'Davis', 'Robbie', 'Cavill', 'Coleman', 'Redmayne', 'Jordan', 'Swinton', 'Stone', 'Hiddleston', 'Statham',
        'Reynolds', 'Fox', 'Sandler', 'Efron', 'Phoenix', 'Mendes', 'Blunt', 'Bardem', 'Hathaway', 'Adams',
        'Hayek', 'Affleck', 'Ledger', 'Hemsworth', 'Momoa', 'Leto', 'Theron', 'Hardy', 'Maguire', 'Washington',
        'McAdams', 'Dallas Howard', 'Elba', 'Winslet', 'Bloom', 'Portman', 'Cumberbatch', 'Stewart', 'LaBeouf', 'Eilish',
        'Berry', 'Law', 'Diesel', 'Ridley', 'Witherspoon', 'Tennant', 'Tatum', 'Chalamet', 'Kravitz', 'Johansson',
        'Cena', 'Barrymore', 'Kunis', 'Momoa', 'Olsen', 'Murphy', 'Pugh', 'Evans', 'Holland', 'Cruz'
    ];

    // Randomly select a first name and last name from each list
    const randomFirstName: string = firstNames[Math.floor(Math.random() * firstNames.length)];
    const randomLastName: string = lastNames[Math.floor(Math.random() * lastNames.length)];

    // Combine the selected first name and last name
    const celebrityName: string = `${randomFirstName} ${randomLastName}`;

    return celebrityName;
}
