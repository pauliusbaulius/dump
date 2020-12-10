export function convertNumberToEnglishText(n: number): string {
    /**
     * Returns a string representation of a number in English.
     * Calls recursive translator if the given number is not 0, otherwise it returns 0 directly.
     * @param {number} n The number to translate into English.
     * @return {string} n translation in words. For example n=10 will return "eleven".
     */

    if (n == 0) {
        return "zero";
    } else {
        return recursiveTranslation(n);
    }
}

const recursiveTranslation = (n: number): string => {
    /**
     * Returns a string representation of a number in English that is not zero.
     * Uses a pretty simple algorithm of floor division and modulo operators.
     * Handles numbers up to one hundred thousand.
     * Can be extended to handle arbitrary sized numbers, but is not the optimal algorithm, due to recursive approach.
     * @param {number} n The number to translate into English.
     * @return {string} n translation in words. For example n=10 will return "eleven".
     */

    // Zero is blank, because it is not used in composed words, only when the number is 0.
    const lt20 = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thriteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    // Zero is not needed here, and ten will be taken from lt20.
    const lt100 = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    // If the number is negative.
    if (n < 0) {
        return "negative " + convertNumberToEnglishText(-n);
    }

    if (n < 20) {
        return lt20[n];
    }

    if (n < 100) {
        const x = lt100[Math.floor(n / 10)]
        const y = lt20[Math.floor(n % 10)]
        if (y) {
            return `${x} ${y}`
        } else {
            return x
        }
    }

    if (n < 1000) {
        const x = lt20[Math.floor(n / 100)]
        const y = recursiveTranslation(Math.floor(n % 100))
        return stringifyNumbers(x, y, "hundred")
    }

    if (n < 100000) {xd
        const x = recursiveTranslation(Math.floor(n / 1000))
        const y = recursiveTranslation(Math.floor(n % 1000))
        return stringifyNumbers(x, y, "thousand")
    }

}

const stringifyNumbers = (x: number, y: number, z: string): string => {
    /**
    * Handles the case where you need to add additional word and fix whitespace between them.
    * 40.000 is fourty thousand, but 40.001 is fourty thousand one.
    * @param {number} x The major number
    * @param {number} y The minor number
    * @param {string} z The unit
    * @return {string} Major (and minor) number joined with unit.
    *
    */
    if (y) {
        return `${x} ${z} ${y}`
    } else {
        return `${x} ${z}`
    }
}
