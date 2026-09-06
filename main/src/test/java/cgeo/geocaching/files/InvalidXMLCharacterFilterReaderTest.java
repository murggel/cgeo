package cgeo.geocaching.files;

import java.io.IOException;
import java.io.StringReader;

import org.junit.Test;
import static org.assertj.core.api.Assertions.assertThat;

public class InvalidXMLCharacterFilterReaderTest {

    private static String filter(final String input) throws IOException {
        final InvalidXMLCharacterFilterReader reader = new InvalidXMLCharacterFilterReader(new StringReader(input));
        final char[] buf = new char[input.length() + 10];
        final int n = reader.read(buf, 0, buf.length);
        if (n <= 0) {
            return "";
        }
        return new String(buf, 0, n);
    }

    @Test
    public void testValidAsciiPassesThrough() throws IOException {
        assertThat(filter("hello world")).isEqualTo("hello world");
    }

    @Test
    public void testInvalidXmlCharIsFiltered() throws IOException {
        // U+000B (vertical tab) is not a valid XML character
        assertThat(filter("invalid\u000Bchar")).isEqualTo("invalidchar");
    }

    @Test
    public void testSurrogatePairPassesThrough() throws IOException {
        final String emojis = "\uD83E\uDD86\uD83D\uDE80\uD83C\uDF0D";
        assertThat(filter("before" + emojis + "after")).isEqualTo("before" + emojis + "after");
    }
}

