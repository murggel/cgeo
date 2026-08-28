# c:geo – GitHub Codespace Cheat-Sheet

## 🛠 Eigene Tasks

Die persönlichen User-Tasks sind **nicht Bestandteil des c:geo-Repositories**.

Öffnen:

**Ctrl+Shift+P → `Tasks: Run Task`**

Aktuelle Tasks:

| Task                  | Funktion                               |
| --------------------- | -------------------------------------- |
| 🔨 Build Basic Debug  | c:geo Debug-Version bauen              |
| ✓ Checkstyle          | Checkstyle-Prüfung                     |
| 🔍 Android Lint       | Lint-Prüfung                           |
| 🧪 Unit Tests (Debug) | Java/JVM-Unit-Tests                    |
| 🚦 Alles prüfen       | Build + Checkstyle + Lint + Unit Tests |

### Gradle-Sync

**Ctrl+Shift+P → `Gradle: Refresh Gradle Project`**

Das ist der Sync der Gradle-Erweiterung.

---

# ☕ Java

Java-Version:

```bash
java -version
```

Gradle/JDK prüfen:

```bash
./gradlew --version
```

Aktuell verwendet der Codespace **JDK 21**.

---

# 🤖 Android SDK

SDK-Verzeichnis:

```text
/opt/android-sdk
```

Variablen:

```bash
echo $ANDROID_HOME
echo $ANDROID_SDK_ROOT
```

Installierte SDK-Komponenten:

```bash
sdkmanager --list_installed
```

Android Debug Bridge:

```bash
adb version
```

SDK Platform:

```bash
ls -d $ANDROID_HOME/platforms/android-36
```

Build Tools:

```bash
ls -d $ANDROID_HOME/build-tools/35.0.0
```

---

# 🐘 Gradle

Immer den **Gradle Wrapper** des Projekts verwenden:

```bash
./gradlew <task>
```

Gradle-Version:

```bash
./gradlew --version
```

Abhängigkeiten neu prüfen:

```bash
./gradlew --refresh-dependencies <task>
```

⚠️ Nur verwenden, wenn wirklich nötig – kann deutlich länger dauern.

---

# 🌿 Git

## Aktuellen Branch anzeigen

```bash
git branch --show-current
```

## Status

```bash
git status
```

## Alle Branches

```bash
git branch -a
```

## Remote-Branches aktualisieren

```bash
git fetch
```

Danach:

```bash
git branch -a
```

## Branch wechseln

```bash
git switch <branch>
```

Beispiel:

```bash
git switch codespaces
```

Wenn der Branch nur remote existiert:

```bash
git switch --track origin/<branch>
```

---

# 🔎 Änderungen kontrollieren

Uncommitted Änderungen:

```bash
git diff
```

Nur geänderte Dateien:

```bash
git status
```

Letzten Commit:

```bash
git log -1 --oneline
```

Kurze Historie:

```bash
git log --oneline -10
```

---

# 💾 Änderungen committen

Dateien vormerken:

```bash
git add <datei>
```

Alle Änderungen:

```bash
git add .
```

Commit:

```bash
git commit -m "Kurze Beschreibung"
```

Nach GitHub übertragen:

```bash
git push
```

---

# 🔄 Änderungen von GitHub holen

Remote-Informationen aktualisieren:

```bash
git fetch
```

Lokalen Branch aktualisieren:

```bash
git pull
```

⚠️ Vor `pull` immer prüfen:

```bash
git status
```

---

# 🚀 Typischer Workflow für eine kleine Änderung

### 1. Branch prüfen

```bash
git branch --show-current
```

### 2. Änderungen holen

```bash
git fetch
```

### 3. Java-Datei bearbeiten

VS Code bietet dabei u. a.:

* Go to Definition
* Find References
* Code Completion
* Rename
* Fehler-/Warnungsanzeige

### 4. Schnell testen

**🧪 Unit Tests (Debug)**

oder:

**🔨 Build Basic Debug**

### 5. Vor dem Commit

**🚦 Alles prüfen**

### 6. Änderungen ansehen

```bash
git status
git diff
```

### 7. Commit

```bash
git add <dateien>
git commit -m "Beschreibung"
```

### 8. Push

```bash
git push
```

---

# 🌐 Mehrere Codespaces

Jeder Codespace hat seinen **eigenen Arbeitsbereich**.

GitHub ist die gemeinsame Quelle:

```text
             GitHub / Fork
              /         \
             /           \
      Codespace 1      Codespace 2
        eigener          eigener
      Arbeitsbereich   Arbeitsbereich
```

Wenn in Codespace 1 ein Branch gepusht wurde:

```bash
git fetch
```

in Codespace 2 ausführen.

Danach kann der Branch dort ausgecheckt werden:

```bash
git switch <branch>
```

### Wichtig

Nicht gleichzeitig unkoordiniert auf demselben Branch in mehreren Codespaces arbeiten.

# 📦Umgang mit dem codespaces-Branch
* Der codespaces-Branch enthält das komplette c:geo-Repository plus .devcontainer/.
* Für normale Arbeiten im Codespace auf den gewünschten Feature-Branch wechseln.
* Der codespaces-Branch muss aktualisiert werden:
   * Codespace-/Buildumgebung hat sich geändert

```bash
git switch codespaces
git fetch upstream
git rebase upstream/master
git push --force-with-lease
```

---
## 📦 APK aus dem Codespace bauen und herunterladen

Eine installierbare Debug-APK kann direkt im Codespace erzeugt werden.

### APK bauen

Im Terminal:

```bash
./gradlew assembleBasicDebug
```

Oder den entsprechenden User-Task **📦 APK bauen** verwenden, falls eingerichtet.

### APK finden

```bash
find main/build/outputs/apk -name "*.apk"
```

Die APK liegt typischerweise unter:

```text
main/build/outputs/apk/basic/debug/
```

### APK auf Tablet/Smartphone übertragen

Die APK befindet sich zunächst **nur im Codespace**.

Im VS-Code-Dateiexplorer zur APK navigieren und die Datei über **Download** auf das Tablet herunterladen.

Anschließend kann die APK wie jede andere Datei auf das Smartphone übertragen und dort installiert werden.

### Wichtig

* Die APK ist eine **Debug-Version** und nicht für die Veröffentlichung gedacht.
* Sie kann zum Testen auf einem Android-Gerät verwendet werden.
* Wenn der Codespace gelöscht wird, sind dort erzeugte Build-Dateien ebenfalls weg. Benötigte APKs daher vorher herunterladen.
* Die APK muss nicht ins Git-Repository eingecheckt werden.

---

# ⏸ Codespace pausieren

Wenn du nicht mehr arbeitest:

**Codespace stoppen**

Nicht nur den Browser-Tab schließen.

Die automatische Inaktivitätsabschaltung ist zusätzlich eingestellt.

⚠️ Ein laufender Gradle-Build sollte nicht einfach durch die automatische Abschaltung unterbrochen werden.

# 🧹 Was wir NICHT benötigen

Für unseren c:geo-Codespace:

* ❌ Android Studio
* ❌ Android Emulator
* ❌ NDK
* ❌ CMake
* ❌ Kotlin-Unterstützung
* ❌ c:geo-spezifische VS-Code-Extension

Der Codespace ist für **Java-Entwicklung, Gradle, Tests und PR-Arbeit** ausgelegt.

---

# 🆘 Nützliche Diagnosebefehle

## Betriebssystem

```bash
cat /etc/os-release
```

## Benutzer

```bash
whoami
```

## Java

```bash
which java
java -version
```

## Gradle

```bash
./gradlew --version
```

## Android SDK

```bash
echo $ANDROID_HOME
which sdkmanager
sdkmanager --version
adb version
```

## Git

```bash
git status
git branch --show-current
git remote -v
```

---

# ⭐ Die wichtigsten fünf Dinge

Wenn du nur das Wesentliche behalten möchtest:

**Task starten**

```text
Ctrl+Shift+P
→ Tasks: Run Task
```

**Gradle synchronisieren**

```text
Ctrl+Shift+P
→ Gradle: Refresh Gradle Project
```

**Branch prüfen**

```bash
git branch --show-current
```

**Änderungen prüfen**

```bash
git status
git diff
```

**Alles testen**

```text
🚦 Alles prüfen
```
