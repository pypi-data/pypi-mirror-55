#include "Firebase.h"
#include "firebase/app.h"
#include "firebase/future.h"
#include "firebase/admob.h"

#ifdef _WIN32
#include <windows.h>
#include <stdarg.h>

void LogMessage(const char* format, ...) {
	va_list list;
	va_start(list, format);
	vprintf(format, list);
	va_end(list);
	printf("\n");
	fflush(stdout);
}

WindowContext FirebaseGetWindowContext()
{
	return nullptr;
}

#elif defined(__ANDROID__)
#include <unistd.h>
#include <jni.h>

JavaVM* g_jvm;
jclass g_classActivity = nullptr;
jfieldID g_jfieldInstanceActivity = nullptr;

bool AndroidFirebase_setJavaVM(JavaVM* vm, const char* activityClass, const char* activityClassName)
{
    g_jvm = vm;
    JNIEnv* env;
    if (g_jvm->GetEnv((void**) &env, JNI_VERSION_1_6) != JNI_OK) {
        return false;
    }

	g_classActivity = reinterpret_cast<jclass>(env->NewGlobalRef(env->FindClass(activityClass)));
	g_jfieldInstanceActivity = env->GetStaticFieldID(g_classActivity, "mainActivityInstance", activityClassName);

    return true;
}

JNIEnv* FirebaseGetJniEnv()
{
	JNIEnv* env;
	int getEnvStat = g_jvm->GetEnv((void**)&env, JNI_VERSION_1_6);
	if (getEnvStat == JNI_EDETACHED)
	{
		if (g_jvm->AttachCurrentThread(&env, NULL) != 0) {
			LOG("Failed to attach env");
			return nullptr;
		}
	}
	else if (getEnvStat == JNI_EVERSION) {
		LOG("GetEnv: version not supported");
		return nullptr;
	}
	return env;
}

jobject FirebaseGetActivity()
{
    JNIEnv* env = FirebaseGetJniEnv();
	return env->GetStaticObjectField(g_classActivity, g_jfieldInstanceActivity);
}

// Get the window context. For Android, it's a jobject pointing to the Activity.
jobject FirebaseGetWindowContext()
{
	return FirebaseGetActivity();
}

#endif

::firebase::App* Firebase::firebase_app = nullptr;

Firebase::Firebase()
{
}
Firebase::~Firebase()
{
}

void Firebase::init()
{
	firebase_app = ::firebase::App::GetInstance();

	if (firebase_app == nullptr)
	{
		LOG("Initialize the Firebase library");
#if defined(__ANDROID__)
		firebase_app = ::firebase::App::Create(FirebaseGetJniEnv(), FirebaseGetActivity());

		g_jvm->DetachCurrentThread();
#else
		firebase_app = ::firebase::App::Create();
#endif  // defined(__ANDROID__)
	}
	
	LOG("fb.initCreated the firebase app %x", static_cast<int>(reinterpret_cast<intptr_t>(firebase_app)));	
	
}

void Firebase::release()
{
	LOG("release");
	delete firebase_app;
#if __ANDROID__
	g_jvm->DetachCurrentThread();
#endif  // defined(__ANDROID__)
}

bool Firebase::ProcessEvents(int msec)
{
#ifdef _WIN32
	Sleep(msec);
#else
	usleep(msec * 1000);
#endif  // _WIN32
	return true;
}

void Firebase::WaitForFutureCompletion(firebase::FutureBase future, int msec)
{
	while (future.status() == ::firebase::kFutureStatusPending) {
		if (ProcessEvents(msec)) return;
	}

	if (future.error() != firebase::admob::kAdMobErrorNone) {
		LOG("ERROR: Action failed with error code %d and message \"%s\".",
			future.error(), future.error_message());
	}
}