package cgeo.geocaching.utils.formulas;

import org.junit.Test;
import static org.assertj.core.api.Java6Assertions.assertThat;
import static org.assertj.core.api.Java6Assertions.assertThatThrownBy;

public class SumFunctionTest {

    @Test
    public void testSumNumericRange() {
        // sum('1-5') -> 1+2+3+4+5 = 15
        final Value result = Formula.evaluate("sum('1-5')");
        assertThat(result.getAsLong()).isEqualTo(15);
    }

    @Test
    public void testSumNumericRangeLarger() {
        // sum('10-100') -> 10+11+12+13+...+100 = 5005
        final Value result = Formula.evaluate("sum('10-100')");
        assertThat(result.getAsLong()).isEqualTo(5005);
    }

    @Test
    public void testSumNumericRangeSingleValue() {
        // sum('5-5') -> 5
        final Value result = Formula.evaluate("sum('5-5')");
        assertThat(result.getAsLong()).isEqualTo(5);
    }

    @Test
    public void testSumSingleLetterVariableRange() {
        // sum('A-D') with A=1, B=2, C=3, D=4 -> 10
        final Value result = Formula.evaluate("sum('A-D')", "A", 1, "B", 2, "C", 3, "D", 4);
        assertThat(result.getAsLong()).isEqualTo(10);
    }

    @Test
    public void testSumSingleLetterVariableRangeWithDollar() {
        // sum('$A-$D') with A=1, B=2, C=3, D=4 -> 10
        final Value result = Formula.evaluate("sum('$A-$D')", "A", 1, "B", 2, "C", 3, "D", 4);
        assertThat(result.getAsLong()).isEqualTo(10);
    }

    @Test
    public void testSumTwoLetterVariableRangeNumericSuffix() {
        // sum('$A1-$A3') with A1=5, A2=10, A3=15 -> 30
        final Value result = Formula.evaluate("sum('$A1-$A3')", "A1", 5, "A2", 10, "A3", 15);
        assertThat(result.getAsLong()).isEqualTo(30);
    }

    @Test
    public void testSumTwoLetterVariableRangeLetterSuffix() {
        // sum('$NA-$NC') with NA=1, NB=2, NC=3 -> 6
        final Value result = Formula.evaluate("sum('$NA-$NC')", "NA", 1, "NB", 2, "NC", 3);
        assertThat(result.getAsLong()).isEqualTo(6);
    }

    @Test
    public void testSumPreCalculatedVariable() {
        // sum('3-5') -> 3+4+5 = 12
        final Value result = Formula.evaluate("sum('3-5')");
        assertThat(result.getAsLong()).isEqualTo(12);
    }

    @Test
    public void testSumNegativeRanges() {
        // Test -3-3 format (without parentheses)
        final Value result1 = Formula.evaluate("sum('-3-3')");
        assertThat(result1.getAsLong()).isEqualTo(0);

        // Test (-3)-(-1) format (with parentheses on both sides)
        final Value result2 = Formula.evaluate("sum('(-3)-(-1)')");
        assertThat(result2.getAsLong()).isEqualTo(-6);

        // Test (-5)-(-2) format
        final Value result3 = Formula.evaluate("sum('(-5)-(-2)')");
        assertThat(result3.getAsLong()).isEqualTo(-14);

        // Test (-3)-3 format (left parenthesis only)
        final Value result4 = Formula.evaluate("sum('(-3)-3')");
        assertThat(result4.getAsLong()).isEqualTo(0);

        // Test -5-(-2) format (right parenthesis only)
        final Value result5 = Formula.evaluate("sum('-5-(-2)')");
        assertThat(result5.getAsLong()).isEqualTo(-14);

        // Test negative to positive range
        final Value result6 = Formula.evaluate("sum('-2-2')");
        assertThat(result6.getAsLong()).isEqualTo(0);

        // Test only negative values
        final Value result7 = Formula.evaluate("sum('-10-(-5)')");
        assertThat(result7.getAsLong()).isEqualTo(-45);
    }

    @Test
    public void testSumErrorMixedTypes() {
        // sum('A-5') -> error: invalid format
        assertThatThrownBy(() -> Formula.evaluate("sum('A-5')", "A", 1))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");
    }

    @Test
    public void testSumErrorMissingVariables() {
        // sum('A-D') with A=1, B=2, C and D not defined -> error
        assertThatThrownBy(() -> Formula.evaluate("sum('A-D')", "A", 1, "B", 2))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("Missing")
                .hasMessageContaining("C")
                .hasMessageContaining("D");
    }

    @Test
    public void testSumErrorMissingVariablesSuffix() {
        // sum('A-D') with A=1, B=2, C and D not defined -> error
        assertThatThrownBy(() -> Formula.evaluate("sum('$NA-$ND')", "NA", 1, "NB", 2))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("Missing")
                .hasMessageContaining("NC")
                .hasMessageContaining("ND");
    }

    @Test
    public void testSumErrorStartGreaterThanEnd() {
        // sum('5-1') -> error: start > end
        assertThatThrownBy(() -> Formula.evaluate("sum('5-1')"))
                .isInstanceOf(FormulaException.class);
    }

    @Test
    public void testSumDependencyTracking() {
        // Verify that sum('A-D') declares all variables A, B, C, D as dependencies
        final Formula formula = Formula.compile("sum('A-D')");
        assertThat(formula.getNeededVariables()).containsExactlyInAnyOrder("A", "B", "C", "D");
    }

    @Test
    public void testSumDependencyTrackingNumericSuffix() {
        // Verify that sum('$A1-$A3') declares A1, A2, A3 as dependencies
        final Formula formula = Formula.compile("sum('$A1-$A3')");
        assertThat(formula.getNeededVariables()).containsExactlyInAnyOrder("A1", "A2", "A3");
    }

    @Test
    public void testSumDependencyTrackingLetterSuffix() {
        // Verify that sum('$NA-$NC') declares NA, NB, NC as dependencies
        final Formula formula = Formula.compile("sum('$NA-$NC')");
        assertThat(formula.getNeededVariables()).containsExactlyInAnyOrder("NA", "NB", "NC");
    }

    @Test
    public void testSumWithDecimalVariables() {
        // sum('A-C') with A=1.5, B=2.5, C=3.0 -> 7.0
        final Value result = Formula.evaluate("sum('A-C')", "A", 1.5, "B", 2.5, "C", 3.0);
        assertThat(result.getAsDouble()).isEqualTo(7.0);
    }

    @Test
    public void testSumSingleLetterVariableRangeLowercase() {
        // sum('a-d') with a=1, b=2, c=3, d=4 -> 10
        final Value result = Formula.evaluate("sum('a-d')", "a", 1, "b", 2, "c", 3, "d", 4);
        assertThat(result.getAsLong()).isEqualTo(10);
    }


    @Test
    public void testSumErrorNonNumericVariable() {
        // sum('A-C') with A=1, B="text", C=3 -> error
        assertThatThrownBy(() -> Formula.evaluate("sum('A-C')", "A", 1, "B", "text", "C", 3))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("WRONG_TYPE");


    }

    @Test
    public void testSumNumericRangeNotInteger() {
        // sum('1.5-5') -> error: must be integer
        assertThatThrownBy(() -> Formula.evaluate("sum('1.5-5')"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("WRONG_TYPE");
    }

    @Test
    public void testSumLowercaseVariables() {
        // sum('a-c') with a=1, b=2, c=3 -> 6
        final Value result = Formula.evaluate("sum('a-c')", "a", 1, "b", 2, "c", 3);
        assertThat(result.getAsLong()).isEqualTo(6);
    }

    @Test
    public void testSumInFormula() {
        // Test sum within a larger formula: sum('1-3') + 10 = 16
        final Value result = Formula.evaluate("sum('1-3') + 10");
        assertThat(result.getAsLong()).isEqualTo(16);
    }

    @Test
    public void testSumVariableRangeInFormula() {
        // Test sum with variables in larger formula: sum('A-B') * 2
        final Value result = Formula.evaluate("sum('A-B') * 2", "A", 3, "B", 4);
        assertThat(result.getAsLong()).isEqualTo(14);
    }


    @Test
    public void testSumMultipleNumericRanges() {
        // sum('1-5'; '10-15') -> (1+2+3+4+5) + (10+11+12+13+14+15) = 15 + 75 = 90
        final Value result = Formula.evaluate("sum('1-5'; '10-15')");
        assertThat(result.getAsLong()).isEqualTo(90);
    }

    @Test
    public void testSumMultipleNumericRangesThreeParams() {
        // sum('1-3'; '10-12'; '20-22') -> (1+2+3) + (10+11+12) + (20+21+22) = 6 + 33 + 63 = 102
        final Value result = Formula.evaluate("sum('1-3'; '10-12'; '20-22')");
        assertThat(result.getAsLong()).isEqualTo(102);
    }

    @Test
    public void testSumMultipleVariableRanges() {
        // sum('A-B'; 'D-E') with A=1, B=2, D=4, E=5 -> (1+2) + (4+5) = 12
        final Value result = Formula.evaluate("sum('A-B'; 'D-E')", "A", 1, "B", 2, "D", 4, "E", 5);
        assertThat(result.getAsLong()).isEqualTo(12);
    }

    @Test
    public void testSumOverlappingVariableRanges() {
        // sum('A-B'; 'D-E') with A=1, B=2, D=4, E=5 -> (1+2) + (4+5) = 12
        final Value result = Formula.evaluate("sum('A-D'; 'C-E')", "A", 1, "B", 2, "C", 3, "D", 4, "E", 5);
        assertThat(result.getAsLong()).isEqualTo(22);
    }

    @Test
    public void testSumMultipleVariableRangesWithDollar() {
        // sum('$A1-$A2'; '$B1-$B2') with A1=1, A2=2, B1=10, B2=20 -> (1+2) + (10+20) = 33
        final Value result = Formula.evaluate("sum('$A1-$A2'; '$NB1-$NB2')", "A1", 1, "A2", 2, "NB1", 10, "NB2", 20);
        assertThat(result.getAsLong()).isEqualTo(33);
    }

    @Test
    public void testSumMultipleDependencyTracking() {
        // Verify that sum('A-C'; 'X-Z') declares all variables A, B, C, X, Y, Z as dependencies
        final Formula formula = Formula.compile("sum('A-C'; 'X-Z')");
        assertThat(formula.getNeededVariables()).containsExactlyInAnyOrder("A", "B", "C", "X", "Y", "Z");
    }

    @Test
    public void testSumMultipleVariableRangesThreeParams() {
        // sum('A-C'; 'E-G'; '20-22') -> (3+4+5) + (6+7+8) + (20+21+22) = 12 + 21 + 63 = 96
        final Value result = Formula.evaluate("sum('A-C'; 'E-G'; '20-22')", "A", 3, "B", 4, "C", 5, "E", 6, "F", 7, "G", 8);
        assertThat(result.getAsLong()).isEqualTo(96);
    }

    @Test
    public void testSumMixedRanges() {
        // sum('A-B'; '10-12') with A=1, B=2 -> (1+2) + (10+11+12) = 3 + 33 = 36
        final Value result = Formula.evaluate("sum('A-B'; '10-12')", "A", 1, "B", 2);
        assertThat(result.getAsLong()).isEqualTo(36);
    }

    @Test
    public void testSumMixedRangesMultiple() {
        // sum('1-3'; 'A-B'; '10-12'; 'X-Y') with A=5, B=6, X=20, Y=21
        // -> (1+2+3) + (5+6) + (10+11+12) + (20+21) = 6 + 11 + 33 + 41 = 91
        final Value result = Formula.evaluate("sum('1-3'; 'A-B'; '10-12'; 'X-Y')", "A", 5, "B", 6, "X", 20, "Y", 21);
        assertThat(result.getAsLong()).isEqualTo(91);
    }

    @Test
    public void testSumMixedRangesDependencyTracking() {
        // Verify that sum('A-C'; '1-5'; 'X-Z') declares only variables A, B, C, X, Y, Z as dependencies (not 1-5)
        final Formula formula = Formula.compile("sum('A-C'; '1-5'; 'X-Z')");
        assertThat(formula.getNeededVariables()).containsExactlyInAnyOrder("A", "B", "C", "X", "Y", "Z");
    }

    @Test
    public void testSumSingleNumericValue() {
        // sum(42) -> 42
        final Value result = Formula.evaluate("sum(42)");
        assertThat(result.getAsLong()).isEqualTo(42);
    }

    @Test
    public void testSumMultipleSingleNumericValues() {
        // sum(1; 5; 10) -> 16
        final Value result = Formula.evaluate("sum(1; 5; 10)");
        assertThat(result.getAsLong()).isEqualTo(16);
    }

    @Test
    public void testSumMixedRangeAndSingleValues() {
        // sum('1-3'; 10; 20) -> (1+2+3) + 10 + 20 = 36
        final Value result = Formula.evaluate("sum('1-3'; 10; 20)");
        assertThat(result.getAsLong()).isEqualTo(36);
    }

    @Test
    public void testSumSingleVariable() {
        // sum(A) with A=10 -> 10
        final Value result = Formula.evaluate("sum(A)", "A", 10);
        assertThat(result.getAsLong()).isEqualTo(10);
    }

    @Test
    public void testSumMultipleSingleVariables() {
        // sum(A; B; C) with A=1, B=2, C=3 -> 6
        final Value result = Formula.evaluate("sum(A; B; C)", "A", 1, "B", 2, "C", 3);
        assertThat(result.getAsLong()).isEqualTo(6);
    }

    @Test
    public void testSumMixedVariableRangeAndSingleVariables() {
        // sum('A-C'; X; Y) with A=1, B=2, C=3, X=10, Y=20 -> (1+2+3) + 10 + 20 = 36
        final Value result = Formula.evaluate("sum('A-C'; X; Y)", "A", 1, "B", 2, "C", 3, "X", 10, "Y", 20);
        assertThat(result.getAsLong()).isEqualTo(36);
    }

    @Test
    public void testSumSingleVariableDependencyTracking() {
        // Verify that sum(A; B; C) declares A, B, C as dependencies
        final Formula formula = Formula.compile("sum(A; B; C)");
        assertThat(formula.getNeededVariables()).containsExactlyInAnyOrder("A", "B", "C");
    }

    @Test
    public void testSumSingleDecimalValue() {
        // sum(10.5) -> 10.5
        final Value result = Formula.evaluate("sum(10.5)");
        assertThat(result.getAsDouble()).isEqualTo(10.5);
    }

    @Test
    public void testSumMultipleDecimalValues() {
        // sum(1.5; 2.5; 3.5) -> 7.5
        final Value result = Formula.evaluate("sum(1.5; 2.5; 3.5)");
        assertThat(result.getAsDouble()).isEqualTo(7.5);
    }

    @Test
    public void testSumMixedIntegerAndDecimalValues() {
        // sum(1; 2.5; 3; 4.5) -> 11
        final Value result = Formula.evaluate("sum(1; 2.5; 3; 4.5)");
        assertThat(result.getAsDouble()).isEqualTo(11.0);
    }

    @Test
    public void testSumMixedRangeAndDecimalValues() {
        // sum('1-3'; 10.5; 20.5) -> (1+2+3) + 10.5 + 20.5 = 37
        final Value result = Formula.evaluate("sum('1-3'; 10.5; 20.5)");
        assertThat(result.getAsDouble()).isEqualTo(37.0);
    }


    @Test
    public void testSumForgottenApostrophe() {
        // sum('1-3'; 10.5; 20.5) -> (1+2+3) + 10.5 + 20.5 = 37
        final Value resultNumeric = Formula.evaluate("sum(1-3)");
        assertThat(resultNumeric.getAsInteger()).isEqualTo(-2);

        final Value resultVariable = Formula.evaluate("sum(A-B)", "A", 5, "B", 2);
        assertThat(resultVariable.getAsInteger()).isEqualTo(3);
    }
}

