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
                <action android:name="com.svitlo.vinnytsia.ACTION_MINUTE_TICK" />
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
    "app/src/main/res/drawable/widget_bg_card.xml": """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="20dp" />
    <gradient
        android:angle="135"
        android:startColor="#0E3A5D"
        android:endColor="#06182B" />
    <stroke
        android:width="1.5dp"
        android:color="#1D6FA5" />
</shape>
""",
    "app/src/main/res/drawable/widget_glow_light_on.xml": """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="14dp" />
    <gradient
        android:angle="90"
        android:startColor="#145A44"
        android:endColor="#0A3326" />
    <stroke
        android:width="1.5dp"
        android:color="#34D399" />
</shape>
""",
    "app/src/main/res/drawable/widget_glow_outage.xml": """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="14dp" />
    <gradient
        android:angle="90"
        android:startColor="#6E1B24"
        android:endColor="#3D0E14" />
    <stroke
        android:width="1.5dp"
        android:color="#F87171" />
</shape>
""",
    "app/src/main/res/drawable/widget_glow_neutral.xml": """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="14dp" />
    <gradient
        android:angle="90"
        android:startColor="#5C4012"
        android:endColor="#332208" />
    <stroke
        android:width="1.5dp"
        android:color="#FBBF24" />
</shape>
""",
    "app/src/main/res/drawable/widget_pill_tag.xml": """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="999dp" />
    <solid android:color="#13466E" />
</shape>
""",
    "app/src/main/res/layout/widget_layout.xml": """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/widgetRoot"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@drawable/widget_bg_card"
    android:gravity="center_horizontal"
    android:orientation="vertical"
    android:padding="10dp">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:gravity="center_vertical"
        android:orientation="horizontal">

        <TextView
            android:id="@+id/tvWidgetTag"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:background="@drawable/widget_pill_tag"
            android:paddingHorizontal="8dp"
            android:paddingVertical="2dp"
            android:text="Черга 2.2"
            android:textColor="#7DD3FC"
            android:textSize="11sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/tvWidgetAddress"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_marginHorizontal="6dp"
            android:layout_weight="1"
            android:ellipsize="end"
            android:gravity="center"
            android:maxLines="1"
            android:text="Шаргород"
            android:textColor="#BAE6FD"
            android:textSize="10sp" />

        <TextView
            android:id="@+id/btnWidgetRefresh"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:background="@drawable/widget_pill_tag"
            android:paddingHorizontal="8dp"
            android:paddingVertical="2dp"
            android:text="↻"
            android:textColor="#F0F9FF"
            android:textSize="14sp"
            android:textStyle="bold" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/widgetGlowBox"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_marginTop="6dp"
        android:layout_weight="1"
        android:background="@drawable/widget_glow_neutral"
        android:gravity="center"
        android:orientation="vertical"
        android:paddingHorizontal="8dp"
        android:paddingVertical="6dp">

        <TextView
            android:id="@+id/tvWidgetStatus"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:gravity="center"
            android:maxLines="1"
            android:text="💡 Світло є"
            android:textColor="#4ADE80"
            android:textSize="17sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/tvWidgetEventTime"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="2dp"
            android:gravity="center"
            android:maxLines="1"
            android:text="Вимкнення о 22:00"
            android:textColor="#4ADE80"
            android:textSize="13sp"
            android:textStyle="bold" />

        <TextView
            android:id="@+id/tvWidgetCountdown"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="2dp"
            android:gravity="center"
            android:maxLines="1"
            android:text="Залишилось: 2 год 33 хв"
            android:textColor="#86EFAC"
            android:textSize="13sp"
            android:textStyle="bold" />
    </LinearLayout>
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
            android:hint="Населений пункт (наприклад, Шаргород)"
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

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="10dp"
            android:orientation="horizontal">

            <Button
                android:id="@+id/btnReloadSite"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_marginEnd="6dp"
                android:layout_weight="1"
                android:text="Оновити сайт" />

            <Button
                android:id="@+id/btnFetch"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_marginStart="6dp"
                android:layout_weight="1"
                android:text="Розпарсити зі сторінки" />
        </LinearLayout>

        <WebView
            android:id="@+id/webView"
            android:layout_width="match_parent"
            android:layout_height="260dp"
            android:layout_marginTop="10dp" />

        <EditText
            android:id="@+id/etIntervals"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="10dp"
            android:hint="Інтервали відключень (наприклад: 08:00-12:00, 18:00-22:00)"
            android:inputType="text" />

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
            android:layout_marginTop="12dp"
            android:text="Статус: зачекайте перевірку безпеки та натисніть Оновити сайт" />
    </LinearLayout>
</ScrollView>
""",
    "app/src/main/java/com/svitlo/vinnytsia/ScheduleParser.kt": """package com.svitlo.vinnytsia

import java.util.Calendar
import java.util.Locale

data class TimeWindow(val startMinutes: Int, val endMinutes: Int)

data class WidgetState(
    val isOutageNow: Boolean,
    val minutesLeft: Int,
    val eventTimeText: String,
    val countdownText: String,
    val rawIntervals: String
)

object ScheduleParser {

    fun parseFromPageText(rawPageText: String, queueTag: String, city: String, street: String, house: String): Pair<List<TimeWindow>, String> {
        val unescaped = unescapeJsString(rawPageText)
        val normalized = unescaped.replace(Regex("\\\\s+"), " ").trim()
        if (normalized.isEmpty()) {
            return Pair(emptyList(), "Сторінка ще порожня або не завантажилась")
        }

        val hourSlots = extractHourSlots(normalized)
        if (hourSlots.isNotEmpty()) {
            return Pair(hourSlots, "Розпарсено годинні інтервали (${hourSlots.size})")
        }

        val addressParts = listOf(city, street, house)
            .map { it.trim().lowercase(Locale.getDefault()) }
            .filter { it.isNotEmpty() }

        val scoped = extractRelevantSection(normalized, queueTag, addressParts)
        val windows = parseWindowsFromText(scoped ?: normalized)
        return if (windows.isNotEmpty()) {
            val sourceLabel = if (scoped != null) "знайдено у фрагменті адреси/черги" else "знайдено на сторінці"
            Pair(windows, "Інтервали розпарсено ($sourceLabel)")
        } else {
            Pair(emptyList(), "На відкритій сторінці інтервали не знайдено")
        }
    }

    private fun extractHourSlots(text: String): List<TimeWindow> {
        val slotRegex = Regex(\"\"\"\\b([01]?\\d|2[0-3])\\s*[-–—]\\s*([01]?\\d|2[0-4])\\b\"\"\")
        val slots = mutableListOf<TimeWindow>()
        for (m in slotRegex.findAll(text)) {
            val h1 = m.groupValues[1].toIntOrNull() ?: continue
            val h2 = m.groupValues[2].toIntOrNull() ?: continue
            if (h2 == h1 + 1 && h1 in 0..23 && h2 in 1..24) {
                slots.add(TimeWindow(h1 * 60, h2 * 60))
            }
        }
        if (slots.size < 3) return emptyList()
        return slots.distinctBy { it.startMinutes to it.endMinutes }.sortedBy { it.startMinutes }
    }

    private fun unescapeJsString(input: String): String {
        val trimmed = input.trim()
        val unwrapped = if (trimmed.startsWith("\\"") && trimmed.endsWith("\\"") && trimmed.length >= 2) {
            trimmed.substring(1, trimmed.length - 1)
        } else {
            trimmed
        }
        return unwrapped
            .replace("\\\\n", "\\n")
            .replace("\\\\r", "\\r")
            .replace("\\\\t", "\\t")
            .replace("\\\\\\"", "\\"")
    }

    private fun extractRelevantSection(text: String, queueTag: String, addressParts: List<String>): String? {
        val lower = text.lowercase(Locale.getDefault())
        for (part in addressParts) {
            val idx = lower.indexOf(part)
            if (idx >= 0) {
                val start = maxOf(0, idx - 80)
                val end = minOf(text.length, idx + 450)
                val slice = text.substring(start, end)
                if (parseWindowsFromText(slice).isNotEmpty()) {
                    return slice
                }
            }
        }

        val tagLower = queueTag.trim().lowercase(Locale.getDefault())
        if (tagLower.isNotEmpty()) {
            val idxTag = lower.indexOf(tagLower)
            if (idxTag >= 0) {
                val start = maxOf(0, idxTag - 40)
                val end = minOf(text.length, idxTag + 350)
                val slice = text.substring(start, end)
                if (parseWindowsFromText(slice).isNotEmpty()) {
                    return slice
                }
            }
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

    private fun fmtMin(minutes: Int): String {
        val clamped = minutes.coerceIn(0, 1440)
        val h = clamped / 60
        val m = clamped % 60
        return String.format(Locale.US, "%02d:%02d", h, m)
    }

    fun formatWindows(windows: List<TimeWindow>): String {
        return windows.joinToString(", ") { w ->
            "${fmtMin(w.startMinutes)}-${fmtMin(w.endMinutes)}"
        }
    }

    fun evaluateNow(windows: List<TimeWindow>): WidgetState {
        val rawStr = formatWindows(windows)
        if (windows.isEmpty()) {
            return WidgetState(
                isOutageNow = false,
                minutesLeft = -1,
                eventTimeText = "--:--",
                countdownText = "Натисніть для налаштування",
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
                    eventTimeText = "Увімкнення о ${fmtMin(w.endMinutes)}",
                    countdownText = "Залишилось: ${formatMinutesCountdown(diff)}",
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
                eventTimeText = "Вимкнення о ${fmtMin(nextOutage.startMinutes)}",
                countdownText = "Залишилось: ${formatMinutesCountdown(diff)}",
                rawIntervals = rawStr
            )
        }

        val firstTomorrow = windows.first()
        val diffTomorrow = (1440 - nowMin) + firstTomorrow.startMinutes
        return WidgetState(
            isOutageNow = false,
            minutesLeft = diffTomorrow,
            eventTimeText = "Вимкнення завтра о ${fmtMin(firstTomorrow.startMinutes)}",
            countdownText = "Залишилось: ${formatMinutesCountdown(diffTomorrow)}",
            rawIntervals = rawStr
        )
    }

    fun formatMinutesCountdown(totalMinutes: Int): String {
        if (totalMinutes < 0) return "-- хв"
        val h = totalMinutes / 60
        val m = totalMinutes % 60
        return if (h > 0) "${h} год ${m} хв" else "${m} хв"
    }
}
""",
    "app/src/main/java/com/svitlo/vinnytsia/SvitloWidget.kt": """package com.svitlo.vinnytsia

import android.app.AlarmManager
import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.os.Build
import android.widget.RemoteViews

class SvitloWidget : AppWidgetProvider() {

    override fun onEnabled(context: Context) {
        super.onEnabled(context, )
        scheduleMinuteTick(context)
    }

    override fun onDisabled(context: Context) {
        super.onDisabled(context, )
        cancelMinuteTick(context)
    }

    override fun onUpdate(context: Context, appWidgetManager: AppWidgetManager, appWidgetIds: IntArray) {
        scheduleMinuteTick(context)
        for (id in appWidgetIds) {
            updateSingleWidget(context, appWidgetManager, id)
        }
    }

    override fun onReceive(context: Context, intent: Intent) {
        super.onReceive(context, intent)
        if (
            intent.action == ACTION_REFRESH ||
            intent.action == ACTION_MINUTE_TICK ||
            intent.action == Intent.ACTION_TIME_TICK ||
            intent.action == AppWidgetManager.ACTION_APPWIDGET_UPDATE
        ) {
            val mgr = AppWidgetManager.getInstance(context)
            val ids = mgr.getAppWidgetIds(ComponentName(context, SvitloWidget::class.java))
            if (ids.isNotEmpty()) {
                for (id in ids) {
                    updateSingleWidget(context, mgr, id)
                }
                scheduleMinuteTick(context)
            }
        }
    }

    companion object {
        const val ACTION_REFRESH = "com.svitlo.vinnytsia.ACTION_REFRESH"
        const val ACTION_MINUTE_TICK = "com.svitlo.vinnytsia.ACTION_MINUTE_TICK"

        private fun tickPendingIntent(context: Context): PendingIntent {
            val intent = Intent(context, SvitloWidget::class.java).apply {
                action = ACTION_MINUTE_TICK
            }
            return PendingIntent.getBroadcast(
                context,
                77,
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
        }

        fun scheduleMinuteTick(context: Context) {
            val mgr = AppWidgetManager.getInstance(context)
            val ids = mgr.getAppWidgetIds(ComponentName(context, SvitloWidget::class.java))
            if (ids.isEmpty()) return

            val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as? AlarmManager ?: return
            val triggerAt = System.currentTimeMillis() + 60_000L
            val pi = tickPendingIntent(context)

            try {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    alarmManager.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, triggerAt, pi)
                } else {
                    alarmManager.set(AlarmManager.RTC_WAKEUP, triggerAt, pi)
                }
            } catch (_: SecurityException) {
                alarmManager.set(AlarmManager.RTC_WAKEUP, triggerAt, pi)
            }
        }

        fun cancelMinuteTick(context: Context) {
            val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as? AlarmManager ?: return
            alarmManager.cancel(tickPendingIntent(context))
        }

        fun updateAll(context: Context) {
            val mgr = AppWidgetManager.getInstance(context)
            val ids = mgr.getAppWidgetIds(ComponentName(context, SvitloWidget::class.java))
            if (ids.isNotEmpty()) {
                for (id in ids) {
                    updateSingleWidget(context, mgr, id)
                }
                scheduleMinuteTick(context)
            }
        }

        fun updateSingleWidget(context: Context, mgr: AppWidgetManager, widgetId: Int) {
            val prefs = context.getSharedPreferences("svitlo_prefs", Context.MODE_PRIVATE)
            val queueTag = prefs.getString("queue_tag", "2.2") ?: "2.2"
            val city = prefs.getString("city", "") ?: ""
            val street = prefs.getString("street", "") ?: ""
            val house = prefs.getString("house", "") ?: ""
            val intervalsRaw = prefs.getString("intervals_raw", "") ?: ""

            val windows = ScheduleParser.parseWindowsFromText(intervalsRaw)
            val state = ScheduleParser.evaluateNow(windows)

            val views = RemoteViews(context.packageName, R.layout.widget_layout)
            views.setTextViewText(R.id.tvWidgetTag, "Черга $queueTag")

            val addrLine = listOf(city, street, house).filter { it.isNotBlank() }.joinToString(", ")
            views.setTextViewText(R.id.tvWidgetAddress, if (addrLine.isNotBlank()) addrLine else "Адреса не задана")

            if (windows.isEmpty()) {
                views.setInt(R.id.widgetGlowBox, "setBackgroundResource", R.drawable.widget_glow_neutral)
                views.setTextViewText(R.id.tvWidgetStatus, "⏳ Немає графіка")
                views.setTextColor(R.id.tvWidgetStatus, Color.parseColor("#FBBF24"))
                views.setTextViewText(R.id.tvWidgetEventTime, "--:--")
                views.setTextColor(R.id.tvWidgetEventTime, Color.parseColor("#FBBF24"))
                views.setTextViewText(R.id.tvWidgetCountdown, "Натисніть для налаштування")
                views.setTextColor(R.id.tvWidgetCountdown, Color.parseColor("#FEF08A"))
            } else if (state.isOutageNow) {
                views.setInt(R.id.widgetGlowBox, "setBackgroundResource", R.drawable.widget_glow_outage)
                views.setTextViewText(R.id.tvWidgetStatus, "⚫ Відключено")
                views.setTextColor(R.id.tvWidgetStatus, Color.parseColor("#FF5A6E"))
                views.setTextViewText(R.id.tvWidgetEventTime, state.eventTimeText)
                views.setTextColor(R.id.tvWidgetEventTime, Color.parseColor("#FF5A6E"))
                views.setTextViewText(R.id.tvWidgetCountdown, state.countdownText)
                views.setTextColor(R.id.tvWidgetCountdown, Color.parseColor("#FCA5A5"))
            } else {
                views.setInt(R.id.widgetGlowBox, "setBackgroundResource", R.drawable.widget_glow_light_on)
                views.setTextViewText(R.id.tvWidgetStatus, "💡 Світло є")
                views.setTextColor(R.id.tvWidgetStatus, Color.parseColor("#4ADE80"))
                views.setTextViewText(R.id.tvWidgetEventTime, state.eventTimeText)
                views.setTextColor(R.id.tvWidgetEventTime, Color.parseColor("#4ADE80"))
                views.setTextViewText(R.id.tvWidgetCountdown, state.countdownText)
                views.setTextColor(R.id.tvWidgetCountdown, Color.parseColor("#86EFAC"))
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

import android.annotation.SuppressLint
import android.content.Context
import android.os.Bundle
import android.webkit.CookieManager
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private val targetUrl = "https://disconnection.voe.com.ua/"

    private val tags = listOf(
        "1.1", "1.2", "2.1", "2.2",
        "3.1", "3.2", "4.1", "4.2",
        "5.1", "5.2", "6.1", "6.2"
    )

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        SvitloWidget.updateAll(this)

        val prefs = getSharedPreferences("svitlo_prefs", Context.MODE_PRIVATE)
        val spQueue = findViewById<Spinner>(R.id.spQueue)
        val etCity = findViewById<EditText>(R.id.etCity)
        val etStreet = findViewById<EditText>(R.id.etStreet)
        val etHouse = findViewById<EditText>(R.id.etHouse)
        val btnReloadSite = findViewById<Button>(R.id.btnReloadSite)
        val btnFetch = findViewById<Button>(R.id.btnFetch)
        val webView = findViewById<WebView>(R.id.webView)
        val etIntervals = findViewById<EditText>(R.id.etIntervals)
        val btnSave = findViewById<Button>(R.id.btnSave)
        val tvLog = findViewById<TextView>(R.id.tvLog)

        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, tags)
        spQueue.adapter = adapter

        val savedTag = prefs.getString("queue_tag", "2.2") ?: "2.2"
        val idx = tags.indexOf(savedTag).coerceAtLeast(0)
        spQueue.setSelection(idx)

        etCity.setText(prefs.getString("city", ""))
        etStreet.setText(prefs.getString("street", ""))
        etHouse.setText(prefs.getString("house", ""))
        etIntervals.setText(prefs.getString("intervals_raw", ""))

        CookieManager.getInstance().setAcceptCookie(true)
        CookieManager.getInstance().setAcceptThirdPartyCookies(webView, true)

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            databaseEnabled = true
            loadWithOverviewMode = true
            useWideViewPort = true
        }
        webView.webChromeClient = WebChromeClient()
        webView.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                tvLog.text = "Сторінка завантажена (${url ?: targetUrl}). За потреби оновіть список і натисніть Розпарсити зі сторінки."
            }
        }
        webView.loadUrl(targetUrl)

        btnReloadSite.setOnClickListener {
            tvLog.text = "Оновлення сторінки..."
            webView.reload()
        }

        btnFetch.setOnClickListener {
            val qTag = tags[spQueue.selectedItemPosition]
            val city = etCity.text.toString().trim()
            val street = etStreet.text.toString().trim()
            val house = etHouse.text.toString().trim()

            tvLog.text = "Зчитування інтервалів зі сторінки..."
            webView.evaluateJavascript("(function() { return document.body ? document.body.innerText : ''; })();") { rawResult ->
                val (windows, statusMsg) = ScheduleParser.parseFromPageText(
                    rawResult ?: "",
                    qTag,
                    city,
                    street,
                    house
                )
                val formatted = ScheduleParser.formatWindows(windows)
                if (formatted.isNotEmpty()) {
                    etIntervals.setText(formatted)
                    tvLog.text = "$statusMsg\\nІнтервали: $formatted"
                } else {
                    tvLog.text = "$statusMsg\\nМожете ввести інтервали вручну (напр. 09:00-13:00)"
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
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Done")
