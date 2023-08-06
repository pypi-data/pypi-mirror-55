#pragma once

#include <stdio.h>
#include <assert.h>
#include <stdint.h>



#ifdef _WIN32
#define IGE_EXPORT __declspec(dllexport)
#else
#define IGE_EXPORT
#endif

#ifdef __ANDROID__
#include <jni.h>
#include <android/log.h>

#define LOG_VERBOSE(...) __android_log_print(ANDROID_LOG_VERBOSE, "firebase", __VA_ARGS__);
#define LOG_DEBUG(...) __android_log_print(ANDROID_LOG_DEBUG, "firebase", __VA_ARGS__);
#define LOG(...) __android_log_print(ANDROID_LOG_INFO, "firebase", __VA_ARGS__);
#define LOG_WARN(...) __android_log_print(ANDROID_LOG_WARN, "firebase", __VA_ARGS__);
#define LOG_ERROR(...) __android_log_print(ANDROID_LOG_ERROR, "firebase", __VA_ARGS__);
#else

void LogMessage(const char* format, ...);

#define LOG_VERBOSE(...) LogMessage(__VA_ARGS__);
#define LOG_DEBUG(...) LogMessage(__VA_ARGS__);
#define LOG(...) LogMessage(__VA_ARGS__);
#define LOG_WARN(...) LogMessage(__VA_ARGS__);
#define LOG_ERROR(...) LogMessage(__VA_ARGS__);
#endif

// WindowContext represents the handle to the parent window.  It's type
// (and usage) vary based on the OS.
#if defined(__ANDROID__)
typedef jobject WindowContext;  // A jobject to the Java Activity.
#elif defined(__APPLE__)
typedef id WindowContext;  // A pointer to an iOS UIView.
#else
typedef void* WindowContext;  // A void* for any other environments.
#endif

namespace firebase
{
	class FutureBase;
	class App;
}

class IGE_EXPORT Firebase
{
public:
	Firebase();
	~Firebase();
	void init();
	void release();

protected:
	static bool ProcessEvents(int msec);
	static void WaitForFutureCompletion(firebase::FutureBase future, int msec = 1000);

	static firebase::App* firebase_app;
};