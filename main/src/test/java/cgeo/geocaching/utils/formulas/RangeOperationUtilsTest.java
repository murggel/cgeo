package cgeo.geocaching.utils.formulas;

import java.util.Arrays;
import java.util.Collection;
import java.util.List;

import org.junit.Test;
import static org.assertj.core.api.Java6Assertions.assertThat;
import static org.assertj.core.api.Java6Assertions.assertThatThrownBy;

public class RangeOperationUtilsTest {

    // ========== getVariableRange() tests ==========
    @Test
    public void testGetNumericRange() {
        final Collection<Value> resultSingleDigit = RangeOperationUtils.getValueRange("1-4");
        assertThat(resultSingleDigit).isEqualTo(Arrays.asList(Value.of(1), Value.of(2), Value.of(3), Value.of(4)));

        final Collection<Value> resultMultiDigit = RangeOperationUtils.getValueRange("19-22");
        assertThat(resultMultiDigit).isEqualTo(Arrays.asList(Value.of(19), Value.of(20), Value.of(21), Value.of(22)));

        final Collection<Value> resultNegativeRange = RangeOperationUtils.getValueRange("-3-3");
        assertThat(resultNegativeRange).isEqualTo(Arrays.asList(Value.of(-3), Value.of(-2), Value.of(-1), Value.of(0), Value.of(1), Value.of(2), Value.of(3)));

        final Collection<Value> resultNegativeWithParens = RangeOperationUtils.getValueRange("(-3)-3");
        assertThat(resultNegativeWithParens).isEqualTo(Arrays.asList(Value.of(-3), Value.of(-2), Value.of(-1), Value.of(0), Value.of(1), Value.of(2), Value.of(3)));

        final Collection<Value> resultNegativeDigitEnd = RangeOperationUtils.getValueRange("-5-(-3)");
        assertThat(resultNegativeDigitEnd).isEqualTo(Arrays.asList(Value.of(-5), Value.of(-4), Value.of(-3)));
    }

    @Test
    public void testGetSingleLetterRange() {
        final Collection<Value> resultUppercase = RangeOperationUtils.getValueRange("A-D");
        assertThat(resultUppercase).isEqualTo(Arrays.asList(Value.of("A"), Value.of("B"), Value.of("C"), Value.of("D")));

        final Collection<Value> resultLowercase = RangeOperationUtils.getValueRange("a-d");
        assertThat(resultLowercase).isEqualTo(Arrays.asList(Value.of("a"), Value.of("b"), Value.of("c"), Value.of("d")));

        final Collection<Value> resultDollar = RangeOperationUtils.getValueRange("$A-$D");
        assertThat(resultDollar).isEqualTo(Arrays.asList(Value.of("A"), Value.of("B"), Value.of("C"), Value.of("D")));

        final Collection<Value> resultSingleRange = RangeOperationUtils.getValueRange("X-X");
        assertThat(resultSingleRange).isEqualTo(List.of(Value.of("X")));

        final Collection<Value> resultDollarMix = RangeOperationUtils.getValueRange("A-$D");
        assertThat(resultDollarMix).isEqualTo(Arrays.asList(Value.of("A"), Value.of("B"), Value.of("C"), Value.of("D")));
    }

    @Test
    public void testGetSingleVariable() {
        final Collection<Value> resultChar = RangeOperationUtils.getValueRange("A");
        assertThat(resultChar).isEqualTo(Arrays.asList(Value.of("A")));

        final Collection<Value> resultVariable = RangeOperationUtils.getValueRange("$N1");
        assertThat(resultVariable).isEqualTo(Arrays.asList(Value.of("N1")));

        final Collection<Value> resultInteger = RangeOperationUtils.getValueRange("53");
        assertThat(resultInteger).isEqualTo(Arrays.asList(Value.of(53)));

        final Collection<Value> resultDecimal = RangeOperationUtils.getValueRange("2.4");
        assertThat(resultDecimal).isEqualTo(Arrays.asList(Value.of(2.4)));

        assertThatThrownBy(() -> RangeOperationUtils.getValueRange("text"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("UNEXPECTED_TOKEN");
    }

    @Test
    public void testGetLetterSuffixRange() {
        final Collection<String> resultUppercase = RangeOperationUtils.getVariableRange("$NA-$ND");
        assertThat(resultUppercase).isEqualTo(Arrays.asList("NA", "NB", "NC", "ND"));

        final Collection<String> resultLowercase = RangeOperationUtils.getVariableRange("$na-$nd");
        assertThat(resultLowercase).isEqualTo(Arrays.asList("na", "nb", "nc", "nd"));
    }

    @Test
    public void testGetDollarMismatch() {
        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("A1-A5"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("UNEXPECTED_TOKEN");

        final Collection<String> resultDollarMismatch = RangeOperationUtils.getVariableRange("$-$A");
        assertThat(resultDollarMismatch).isEqualTo(Arrays.asList("-$A"));
    }

    @Test
    public void testGetNumericSuffixRange() {
        final Collection<String> resultX = RangeOperationUtils.getVariableRange("$X8-$X12");
        assertThat(resultX).isEqualTo(Arrays.asList("X8", "X9", "X10", "X11", "X12"));

        final Collection<String> resultX0 = RangeOperationUtils.getVariableRange("$X08-$X12");
        assertThat(resultX0).isEqualTo(Arrays.asList("X08", "X09", "X10", "X11", "X12"));

        final Collection<String> resultXX = RangeOperationUtils.getVariableRange("$XX10-$XX12");
        assertThat(resultXX).isEqualTo(Arrays.asList("XX10", "XX11", "XX12"));

        final Collection<String> resultXXX = RangeOperationUtils.getVariableRange("$Xx99-$Xx101");
        assertThat(resultXXX).isEqualTo(Arrays.asList("Xx99", "Xx100", "Xx101"));

        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("$X12-$X8"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");
    }

    @Test
    public void testGetLetterSuffixRangeLongerPrefix() {
        final Collection<String> resultChar = RangeOperationUtils.getVariableRange("$VARA-$VARC");
        assertThat(resultChar).isEqualTo(Arrays.asList("VARA", "VARB", "VARC"));

        final Collection<String> resultNumber = RangeOperationUtils.getVariableRange("$VAR11-$VAR13");
        assertThat(resultNumber).isEqualTo(Arrays.asList("VAR11", "VAR12", "VAR13"));
    }

    @Test
    public void testGetPrefixMismatch() {
        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("a-D"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");

        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("$NA-$nb"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");

        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("$NA-$MB"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");

        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("$A1-$B5"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");

        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("$A1-$a5"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");

        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("$VARA-$VarC"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");
    }

    @Test
    public void testGetOrderMismatch() {
        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("D-A"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");

        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("$A5-$A1"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");
    }

    @Test
    public void testGetNumericSuffixMismatch() {
        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("$A1-$AB"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");

        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("$NA-$Nc"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");

        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("$A05-$A8"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");

        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("$A5-$A08"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");

        assertThatThrownBy(() -> RangeOperationUtils.getVariableRange("$A05-$A111"))
                .isInstanceOf(FormulaException.class)
                .hasMessageContaining("INVALID_RANGE");
    }

    @Test
    public void testGetEntireAlphabet() {
        final List<String> result = RangeOperationUtils.getVariableRange("A-Z").stream().toList();
        assertThat(result).hasSize(26);
        assertThat(result.get(0)).isEqualTo("A");
        assertThat(result.get(25)).isEqualTo("Z");
    }

    @Test
    public void testGetEntireAlphabetLowercase() {
        final List<String> result = RangeOperationUtils.getVariableRange("a-z").stream().toList();
        assertThat(result).hasSize(26);
        assertThat(result.get(0)).isEqualTo("a");
        assertThat(result.get(25)).isEqualTo("z");
    }

    @Test
    public void testGetVariableRangeWithDollar() {
        // Test that $NA-NC is correctly parsed and expanded
        final Collection<String> result = RangeOperationUtils.getVariableRange("$NA-$NC");
        assertThat(result).isEqualTo(Arrays.asList("NA", "NB", "NC"));
    }
}
