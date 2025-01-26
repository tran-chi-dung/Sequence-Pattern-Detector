document.getElementById("detectPatternButton").addEventListener("click", detectPattern);

function detectPattern() {
    const input = document.getElementById("sequenceInput").value;
    const sequence = input.split(",").map(num => parseFloat(num.trim()));

    if (sequence.length < 2 || sequence.some(isNaN)) {
        document.getElementById("result").innerHTML = '<span class="error">Invalid input. Please enter at least two valid numbers.</span>';
        return;
    }

    let resultText = "<span>No recognizable pattern found.</span>";

    // Tổng các số trong chuỗi
    const sum = sequence.reduce((acc, num) => acc + num, 0);
    resultText += `<br><span>Total sum of the sequence: ${sum}</span>`;

    // Trung bình cộng
    const average = sum / sequence.length;
    resultText += `<br><span>Average of the sequence: ${average}</span>`;

    // Giá trị lớn nhất và nhỏ nhất
    const max = Math.max(...sequence);
    const min = Math.min(...sequence);
    resultText += `<br><span>Maximum value: ${max}, Minimum value: ${min}</span>`;

    // Độ lệch chuẩn (Standard Deviation)
    const variance = sequence.reduce((acc, num) => acc + Math.pow(num - average, 2), 0) / sequence.length;
    const stdDev = Math.sqrt(variance);
    resultText += `<br><span>Standard Deviation: ${stdDev}</span>`;

    // Fibonacci check
    const isFibonacci = (seq) => seq.every((num, i) => i < 2 || num === seq[i - 1] + seq[i - 2]);
    if (isFibonacci(sequence)) {
        resultText += `<br><span>Fibonacci pattern detected: Un = Un-1 + Un-2</span>`;
    }

    // Geometric sequence check
    const isGeometric = (seq) => {
        const ratio = seq[1] / seq[0];
        return seq.every((num, i) => i === 0 || Math.abs(num / seq[i - 1] - ratio) < 1e-6);
    };
    if (isGeometric(sequence)) {
        const ratio = sequence[1] / sequence[0];
        resultText += `<br><span>Geometric pattern detected: Un = ${sequence[0]} * (${ratio})^n</span>`;
    }

    // Arithmetic sequence check
    const calculateDifferences = (seq) => seq.slice(1).map((num, i) => num - seq[i]);
    const firstDifferences = calculateDifferences(sequence);
    if (new Set(firstDifferences).size === 1) {
        const d = firstDifferences[0];
        const a = sequence[0] - d;
        resultText += `<br><span>Arithmetic sequence detected: Un = ${d}n + ${a}</span>`;
    }

    // Polynomial sequence check
    const isPolynomial = (seq) => {
        const diffs = [];
        let currentSeq = seq;
        while (currentSeq.length > 1) {
            currentSeq = calculateDifferences(currentSeq);
            diffs.push(currentSeq);
            if (new Set(currentSeq).size === 1) return diffs.length;
        }
        return null;
    };
    const polynomialOrder = isPolynomial(sequence);
    if (polynomialOrder !== null) {
        resultText += `<br><span>Polynomial pattern detected: Degree = ${polynomialOrder}</span>`;
    }

    // Mixed Arithmetic-Geometric sequence check
    const isMixedArithmeticGeometric = (seq) => {
        const ratio = seq[1] / seq[0];
        const diff = seq[1] - seq[0];
        return seq.every((num, i) => {
            return i === 0 || Math.abs(num - seq[i - 1] - diff) < 1e-6 || Math.abs(num / seq[i - 1] - ratio) < 1e-6;
        });
    };
    if (isMixedArithmeticGeometric(sequence)) {
        resultText += `<br><span>Mixed Arithmetic-Geometric sequence detected</span>`;
    }

    // Prime number check
    const isPrime = (num) => {
        if (num < 2) return false;
        for (let i = 2; i <= Math.sqrt(num); i++) {
            if (num % i === 0) return false;
        }
        return true;
    };
    if (sequence.every(isPrime)) {
        resultText += `<br><span>Prime number sequence detected</span>`;
    }

    // Square number check
    const isSquare = (num) => Number.isInteger(Math.sqrt(num));
    if (sequence.every(isSquare)) {
        resultText += `<br><span>Square number sequence detected</span>`;
    }

    // Cube number check
    const isCube = (num) => Number.isInteger(Math.cbrt(num));
    if (sequence.every(isCube)) {
        resultText += `<br><span>Cube number sequence detected</span>`;
    }

    // Perfect number check
    const isPerfect = (num) => {
        let sum = 0;
        for (let i = 1; i <= Math.sqrt(num); i++) {
            if (num % i === 0) {
                sum += i;
                if (i !== num / i && i !== 1) sum += num / i;
            }
        }
        return sum === num;
    };
    if (sequence.every(isPerfect)) {
        resultText += `<br><span>Perfect number sequence detected</span>`;
    }

    // Monotonic sequence check (increasing or decreasing)
    const isMonotonic = (seq) => {
        const increasing = seq.every((num, i) => i === 0 || num >= seq[i - 1]);
        const decreasing = seq.every((num, i) => i === 0 || num <= seq[i - 1]);
        return increasing || decreasing;
    };
    if (isMonotonic(sequence)) {
        resultText += `<br><span>Monotonic sequence detected (increasing or decreasing)</span>`;
    }

    // Binary sequence check
    const isBinary = (seq) => seq.every(num => num === 0 || num === 1);
    if (isBinary(sequence)) {
        resultText += `<br><span>Binary sequence detected</span>`;
    }

    // Reverse Fibonacci sequence check
    const isReverseFibonacci = (seq) => seq.every((num, i) => i < 2 || num === seq[i - 2] - seq[i - 1]);
    if (isReverseFibonacci(sequence)) {
        resultText += `<br><span>Reverse Fibonacci pattern detected: Un = Un-2 - Un-1</span>`;
    }

    // Exponential sequence check
    const isExponential = (seq) => {
        const ratio = seq[1] / seq[0];
        return seq.every((num, i) => i === 0 || Math.abs(num / seq[i - 1] - ratio) < 1e-6);
    };
    if (isExponential(sequence)) {
        resultText += `<br><span>Exponential pattern detected: Un = U1 * r^n</span>`;
    }

    // Constant sequence check
    const isConstant = (seq) => new Set(seq).size === 1;
    if (isConstant(sequence)) {
        resultText += `<br><span>Constant sequence detected: Un = ${sequence[0]}</span>`;
    }

    // Save to history
    const historyList = document.getElementById("historyList");
    const listItem = document.createElement("li");
    listItem.textContent = `Sequence: ${sequence.join(", ")} → ${resultText.replace(/<[^>]+>/g, '')}`;
    historyList.appendChild(listItem);

    // Display result
    document.getElementById("result").innerHTML = resultText;
}