const fs = require('fs')

fs.readFile('five_letter_words.txt', 'utf8', (err, data) => {
    if (err) throw err;

    console.log(data);
});
