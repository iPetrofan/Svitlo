import os

files = {
    "settings.gradle.kts": """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "SvitloWidget"
include(":app")
""",
    "build.gradle.kts": """plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
}
""",
    "gradle.properties": """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
""",
    "app/build.gradle.kts": """plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.svitlo.vinnytsia"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.svitlo.vinnytsia"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.work:work-runtime-ktx:2.9.1")
}
""",
    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:allowBackup="true"
        android:label="Світло ВОЕ"
        android:supportsRtl="true"
        android:theme="@style/Theme.Material3.DayNight.NoActionBar">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <receiver
            android:name=".SvitloWidget"
            android:exported="true">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
                <action android:name="com.svitlo.vinnytsia.ACTION_REFRESH" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/svitlo_widget_info" />
        </receiver>
    </application>
</manifest>
""",
    "app/src/main/res/xml/svitlo_widget_info.xml": """<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:initialLayout="@layout/widget_layout"
    android:minWidth="180dp"
    android:minHeight="110dp"
    android:resizeMode="horizontal|vertical"
    android:updatePeriodMillis="900000"
    android:widgetCategory="home_screen" />
""",
    "app/src/main/res/layout/widget_layout.xml": """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/widgetRoot"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#111827"
    android:orientation="vertical"
    android:padding="12dp">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal">

        <TextView
            android:id="@+id/tvWidgetTag"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="Черга 1.1"
            android:textColor="#93C5FD"
            android:textSize="12sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/btnWidgetRefresh"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:paddingStart="8dp"
            android:text="↻"
            android:textColor="#E5E7EB"
            android:textSize="16sp" />
    </LinearLayout>

    <TextView
        android:id="@+id/tvWidgetAddress"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:ellipsize="end"
        android:maxLines="1"
        android:text="Адреса не задана"
        android:textColor="#9CA3AF"
        android:textSize="11sp" />

    <TextView
        android:id="@+id/tvWidgetStatus"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="4dp"
        android:text="Оновлення..."
        android:textColor="#FFFFFF"
        android:textSize="15sp"
        android:textStyle="bold" />

    <TextView
        android:id="@+id/tvWidgetCountdown"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="2dp"
        android:text="-- год -- хв"
        android:textColor="#34D399"
        android:textSize="18sp"
        android:textStyle="bold" />
</LinearLayout>
""",
    "app/src/main/res/layout/activity_main.xml": """<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="16dp">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical">

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Віджет світла — Вінницяобленерго"
            android:textSize="20sp"
            android:textStyle="bold" />

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="12dp"
            android:text="Черга / підчерга (тег)"
            android:textStyle="bold" />

        <Spinner
            android:id="@+id/spQueue"
            android:layout_width="match_parent"
            android:layout_height="48dp" />

        <EditText
            android:id="@+id/etCity"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="8dp"
            android:hint="Населений пункт (наприклад, м. Вінниця або Шаргород)"
            android:inputType="text" />

        <EditText
            android:id="@+id/etStreet"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="8dp"
            android:hint="Вулиця"
            android:inputType="text" />

        <EditText
            android:id="@+id/etHouse"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="8dp"
            android:hint="Номер будинку"
            android:inputType="text" />

        <EditText
            android:id="@+id/etIntervals"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="12dp"
            android:hint="Інтервали відключень (наприклад: 08:00-12:00, 18:00-22:00)"
            android:inputType="text" />

        <Button
            android:id="@+id/btnFetch"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="12dp"
            android:text="Отримати і розпарсити графік" />

        <Button
            android:id="@+id/btnSave"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="8dp"
            android:text="Зберегти і оновити віджет" />

        <TextView
            android:id="@+id/tvLog"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="14dp"
            android:text="Статус: очікування дій" />
    </LinearLayout>
</ScrollView>
""",
    "app/src/main/java/com/svitlo/vinnytsia/ScheduleParser.kt": """package com.svitlo.vinnytsia

import java.net.HttpURLConnection
import java.net.URL
import java.util.Calendar
import java.util.Locale

data class TimeWindow(val startMinutes: Int, val endMinutes: Int)

data class WidgetState(
    val isOutageNow: Boolean,
    val minutesLeft: Int,
    val nextEventText: String,
    val rawIntervals: String
)

object ScheduleParser {

    private val candidateUrls = listOf(
        "https://www.voe.com.ua/disconnections/one-page",
        "https://www.voe.com.ua/disconnections",
        "https://voe.com.ua/disconnections"
    )

    fun fetchAndParseIntervals(queueTag: String, city: String, street: String, house: String): Pair<List<TimeWindow>, String> {
        var lastError = "Дані не знайдено"
        for (urlStr in candidateUrls) {
            try {
                val conn = (URL(urlStr).openConnection() as HttpURLConnection).apply {
                    connectTimeout = 8000
                    readTimeout = 8000
                    requestMethod = "GET"
                    setRequestProperty("User-Agent", "Mozilla/5.0")
                }
                if (conn.responseCode in 200..299) {
                    val body = conn.inputStream.bufferedReader().use { it.readText() }
                    val cleanText = body.replace(Regex("<[^>]*>"), " ")
                    val addressNeedle = listOf(city, street, house)
                        .map { it.trim().lowercase(Locale.getDefault()) }
                        .filter { it.isNotEmpty() }

                    val matchedQueue = extractQueueFromText(cleanText, queueTag, addressNeedle)
                    val windows = parseWindowsFromText(matchedQueue ?: cleanText)
                    if (windows.isNotEmpty()) {
                        return Pair(windows, "Завантажено з $urlStr")
                    }
                    lastError = "Сторінку отримано ($urlStr), але інтервали не розпізнано"
                } else {
                    lastError = "HTTP ${conn.responseCode} на $urlStr"
                }
                conn.disconnect()
            } catch (e: Exception) {
                lastError = e.message ?: "Помилка мережі"
            }
        }
        return Pair(emptyList(), lastError)
    }

    private fun extractQueueFromText(text: String, queueTag: String, addressParts: List<String>): String? {
        val lower = text.lowercase(Locale.getDefault())
        if (addressParts.isNotEmpty()) {
            val idxAddr = lower.indexOf(addressParts.first())
            if (idxAddr >= 0) {
                val start = maxOf(0, idxAddr - 120)
                val end = minOf(text.length, idxAddr + 400)
                return text.substring(start, end)
            }
        }
        val tagLower = queueTag.lowercase(Locale.getDefault())
        val idxTag = lower.indexOf(tagLower)
        if (idxTag >= 0) {
            val start = maxOf(0, idxTag - 40)
            val end = minOf(text.length, idxTag + 350)
            return text.substring(start, end)
        }
        return null
    }

    fun parseWindowsFromText(source: String): List<TimeWindow> {
        val regex = Regex(\"\"\"(\\d{1,2})[:.](\\d{2})\\s*[-–—]\\s*(\\d{1,2})[:.](\\d{2})\"\"\")
        val result = mutableListOf<TimeWindow>()
        for (m in regex.findAll(source)) {
            val sh = m.groupValues[1].toIntOrNull() ?: continue
            val sm = m.groupValues[2].toIntOrNull() ?: continue
            val eh = m.groupValues[3].toIntOrNull() ?: continue
            val em = m.groupValues[4].toIntOrNull() ?: continue
            if (sh in 0..24 && eh in 0..24 && sm in 0..59 && em in 0..59) {
                val startMin = sh * 60 + sm
                val endMin = if (eh == 24 && em == 0) 1440 else eh * 60 + em
                if (endMin > startMin) {
                    result.add(TimeWindow(startMin, endMin))
                }
            }
        }
        return result.distinctBy { it.startMinutes to it.endMinutes }.sortedBy { it.startMinutes }
    }

    fun formatWindows(windows: List<TimeWindow>): String {
        return windows.joinToString(", ") { w ->
            String.format(Locale.US, "%02d:%02d-%02d:%02d", w.startMinutes / 60, w.startMinutes % 60, w.endMinutes / 60, w.endMinutes % 60)
        }
    }

    fun evaluateNow(windows: List<TimeWindow>): WidgetState {
        val rawStr = formatWindows(windows)
        if (windows.isEmpty()) {
            return WidgetState(
                isOutageNow = false,
                minutesLeft = -1,
                nextEventText = "Немає даних графіка",
                rawIntervals = ""
            )
        }

        val cal = Calendar.getInstance()
        val nowMin = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)

        for (w in windows) {
            if (nowMin in w.startMinutes until w.endMinutes) {
                val diff = w.endMinutes - nowMin
                return WidgetState(
                    isOutageNow = true,
                    minutesLeft = diff,
                    nextEventText = String.format(Locale.US, "Увімкнення о %02d:%02d", w.endMinutes / 60, w.endMinutes % 60),
                    rawIntervals = rawStr
                )
            }
        }

        val nextOutage = windows.firstOrNull { it.startMinutes > nowMin }
        if (nextOutage != null) {
            val diff = nextOutage.startMinutes - nowMin
            return WidgetState(
                isOutageNow = false,
                minutesLeft = diff,
                nextEventText = String.format(Locale.US, "Вимкнення о %02d:%02d", nextOutage.startMinutes / 60, nextOutage.startMinutes % 60),
                rawIntervals = rawStr
            )
        }

        val firstTomorrow = windows.first()
        val diffTomorrow = (1440 - nowMin) + firstTomorrow.startMinutes
        return WidgetState(
            isOutageNow = false,
            minutesLeft = diffTomorrow,
            nextEventText = String.format(Locale.US, "Вимкнення завтра о %02d:%02d", firstTomorrow.startMinutes / 60, firstTomorrow.startMinutes % 60),
            rawIntervals = rawStr
        )
    }

    fun formatMinutesCountdown(totalMinutes: Int): String {
        if (totalMinutes < 0) return "-- год -- хв"
        val h = totalMinutes / 60
        val m = totalMinutes % 60
        return "${h} год ${m} хв"
    }
}
""",
    "app/src/main/java/com/svitlo/vinnytsia/SvitloWidget.kt": """package com.svitlo.vinnytsia

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.widget.RemoteViews

class SvitloWidget : AppWidgetProvider() {

    override fun onUpdate(context: Context, appWidgetManager: AppWidgetManager, appWidgetIds: IntArray) {
        for (id in appWidgetIds) {
            updateSingleWidget(context, appWidgetManager, id)
        }
    }

    override fun onReceive(context: Context, intent: Intent) {
        super.onReceive(context, intent)
        if (intent.action == ACTION_REFRESH || intent.action == Intent.ACTION_TIME_TICK) {
            val mgr = AppWidgetManager.getInstance(context)
            val ids = mgr.getAppWidgetIds(ComponentName(context, SvitloWidget::class.java))
            onUpdate(context, mgr, ids)
        }
    }

    companion object {
        const val ACTION_REFRESH = "com.svitlo.vinnytsia.ACTION_REFRESH"

        fun updateAll(context: Context) {
            val mgr = AppWidgetManager.getInstance(context)
            val ids = mgr.getAppWidgetIds(ComponentName(context, SvitloWidget::class.java))
            if (ids.isNotEmpty()) {
                val provider = SvitloWidget()
                provider.onUpdate(context, mgr, ids)
            }
        }

        fun updateSingleWidget(context: Context, mgr: AppWidgetManager, widgetId: Int) {
            val prefs = context.getSharedPreferences("svitlo_prefs", Context.MODE_PRIVATE)
            val queueTag = prefs.getString("queue_tag", "1.1") ?: "1.1"
            val city = prefs.getString("city", "") ?: ""
            val street = prefs.getString("street", "") ?: ""
            val house = prefs.getString("house", "") ?: ""
            val intervalsRaw = prefs.getString("intervals_raw", "") ?: ""

            val windows = ScheduleParser.parseWindowsFromText(intervalsRaw)
            val state = ScheduleParser.evaluateNow(windows)

            val views = RemoteViews(context.packageName, R.layout.widget_layout)
            views.setTextViewText(R.id.tvWidgetTag, "Черга $queueTag")

            val addrLine = listOf(city, street, house).filter { it.isNotBlank() }.joinToString(", ")
            views.setTextViewText(R.id.tvWidgetAddress, if (addrLine.isNotBlank()) addrLine else "Адреса не вказана")

            if (windows.isEmpty()) {
                views.setTextViewText(R.id.tvWidgetStatus, "Немає інтервалів")
                views.setTextViewText(R.id.tvWidgetCountdown, "Натисніть для налаштування")
                views.setTextColor(R.id.tvWidgetCountdown, Color.parseColor("#FBBF24"))
            } else if (state.isOutageNow) {
                views.setTextViewText(R.id.tvWidgetStatus, "ВІДКЛЮЧЕННЯ • ${state.nextEventText}")
                views.setTextViewText(R.id.tvWidgetCountdown, "До світла: ${ScheduleParser.formatMinutesCountdown(state.minutesLeft)}")
                views.setTextColor(R.id.tvWidgetCountdown, Color.parseColor("#F87171"))
            } else {
                views.setTextViewText(R.id.tvWidgetStatus, "СВІТЛО Є • ${state.nextEventText}")
                views.setTextViewText(R.id.tvWidgetCountdown, "Залишилось: ${ScheduleParser.formatMinutesCountdown(state.minutesLeft)}")
                views.setTextColor(R.id.tvWidgetCountdown, Color.parseColor("#34D399"))
            }

            val openIntent = Intent(context, MainActivity::class.java)
            val openPending = PendingIntent.getActivity(
                context, 0, openIntent, PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(R.id.widgetRoot, openPending)

            val refreshIntent = Intent(context, SvitloWidget::class.java).apply {
                action = ACTION_REFRESH
            }
            val refreshPending = PendingIntent.getBroadcast(
                context, 1, refreshIntent, PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(R.id.btnWidgetRefresh, refreshPending)

            mgr.updateAppWidget(widgetId, views)
        }
    }
}
""",
    "app/src/main/java/com/svitlo/vinnytsia/MainActivity.kt": """package com.svitlo.vinnytsia

import android.content.Context
import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import java.util.concurrent.Executors

class MainActivity : AppCompatActivity() {

    private val tags = listOf(
        "1.1", "1.2", "2.1", "2.2",
        "3.1", "3.2", "4.1", "4.2",
        "5.1", "5.2", "6.1", "6.2"
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val prefs = getSharedPreferences("svitlo_prefs", Context.MODE_PRIVATE)
        val spQueue = findViewById<Spinner>(R.id.spQueue)
        val etCity = findViewById<EditText>(R.id.etCity)
        val etStreet = findViewById<EditText>(R.id.etStreet)
        val etHouse = findViewById<EditText>(R.id.etHouse)
        val etIntervals = findViewById<EditText>(R.id.etIntervals)
        val btnFetch = findViewById<Button>(R.id.btnFetch)
        val btnSave = findViewById<Button>(R.id.btnSave)
        val tvLog = findViewById<TextView>(R.id.tvLog)

        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, tags)
        spQueue.adapter = adapter

        val savedTag = prefs.getString("queue_tag", "1.1") ?: "1.1"
        val idx = tags.indexOf(savedTag).coerceAtLeast(0)
        spQueue.setSelection(idx)

        etCity.setText(prefs.getString("city", ""))
        etStreet.setText(prefs.getString("street", ""))
        etHouse.setText(prefs.getString("house", ""))
        etIntervals.setText(prefs.getString("intervals_raw", ""))

        val executor = Executors.newSingleThreadExecutor()

        btnFetch.setOnClickListener {
            val qTag = tags[spQueue.selectedItemPosition]
            val city = etCity.text.toString().trim()
            val street = etStreet.text.toString().trim()
            val house = etHouse.text.toString().trim()
            tvLog.text = "Запит до Вінницяобленерго..."

            executor.execute {
                val (windows, statusMsg) = ScheduleParser.fetchAndParseIntervals(qTag, city, street, house)
                val formatted = ScheduleParser.formatWindows(windows)
                runOnUiThread {
                    if (formatted.isNotEmpty()) {
                        etIntervals.setText(formatted)
                        tvLog.text = "$statusMsg\nЗнайдено інтервали: $formatted"
                    } else {
                        tvLog.text = "$statusMsg\nМожете ввести інтервали вручну (напр. 09:00-13:00)"
                    }
                }
            }
        }

        btnSave.setOnClickListener {
            val qTag = tags[spQueue.selectedItemPosition]
            val city = etCity.text.toString().trim()
            val street = etStreet.text.toString().trim()
            val house = etHouse.text.toString().trim()
            val intervalsText = etIntervals.text.toString().trim()

            val parsed = ScheduleParser.parseWindowsFromText(intervalsText)
            val normalized = ScheduleParser.formatWindows(parsed)

            prefs.edit()
                .putString("queue_tag", qTag)
                .putString("city", city)
                .putString("street", street)
                .putString("house", house)
                .putString("intervals_raw", normalized.ifEmpty { intervalsText })
                .apply()

            SvitloWidget.updateAll(this)
            tvLog.text = "Збережено. Інтервали: ${normalized.ifEmpty { "не розпізнано" }}"
        }
    }
}
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Done")
