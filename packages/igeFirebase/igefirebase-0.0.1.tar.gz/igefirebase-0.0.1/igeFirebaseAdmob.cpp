#include "igeFirebase.h"
#include "igeFirebase_doc_en.h"

namespace firebase
{
	extern int pyObjToIntArray(PyObject* obj, uint32_t* idx);
}

PyObject* firebaseAdmob_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	firebaseAdmob_obj* self = NULL;

	self = (firebaseAdmob_obj*)type->tp_alloc(type, 0);
	self->firebaseAdmob = new FirebaseAdmob();

	return (PyObject*)self;
}

void firebaseAdmob_dealloc(firebaseAdmob_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* firebaseAdmob_str(firebaseAdmob_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "firebase admob object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* firebaseAdmob_Init(firebaseAdmob_obj* self, PyObject* args, PyObject* kwargs)
{
	static char* kwlist[] = { "adMobApp","bannerSize", "gender", "childDirectedTreatment","keywords","birthday", "testDevicesIds", NULL };

	PyObject* adMobApp = nullptr;
	PyObject* bannerSize = nullptr;
	PyObject* keywords = nullptr;	
	PyObject* birthday = nullptr;
	PyObject* testDevicesIds = nullptr;
	int gender = 0;
	int childDirectedTreatment;
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OiiOOO", kwlist, &adMobApp, &bannerSize, &gender, &childDirectedTreatment, &keywords, &birthday, &testDevicesIds))return NULL;

	if (adMobApp && PyTuple_Check(adMobApp))
	{
		{
			uint32_t numAttr = 0;
			numAttr = (uint32_t)PyTuple_Size(adMobApp);
			if (numAttr != 4) {
				PyErr_SetString(PyExc_TypeError, "4 Parameters : adMobAppID(char*) | bannerAdUnit(char*) | interstitialAdUnit(char*) | rewardedVideoAdUnit(char*)");
				return NULL;
			}
			const char** paramaters = new const char* [numAttr];
			memset(paramaters, 0, sizeof(char*) * numAttr);
			for (uint32_t i = 0; i < numAttr; i++)
			{
				PyObject* v = PyTuple_GET_ITEM(adMobApp, i);
				paramaters[i] = PyUnicode_AsUTF8(v);
			}
			self->firebaseAdmob->setAdMobApp(paramaters[0], paramaters[1], paramaters[2], paramaters[3]);
		}		
		
		if (bannerSize)
		{
			int bufferSize = firebase::pyObjToIntArray(bannerSize, nullptr);
			if (bufferSize != 2) {
				PyErr_SetString(PyExc_TypeError, "2 Parameters : width(int) | height(int)");
				return NULL;
			}
			uint32_t* buffer = (uint32_t*)malloc(bufferSize * sizeof(int));
			firebase::pyObjToIntArray(bannerSize, buffer);
			self->firebaseAdmob->setBannerSize(buffer[0], buffer[1]);
		}

		{
			self->firebaseAdmob->setGender((firebase::admob::Gender)gender);
		}

		{
			self->firebaseAdmob->setChildDirectedTreatmentState((firebase::admob::ChildDirectedTreatmentState)childDirectedTreatment);
		}

		if (keywords)
		{
			uint32_t numAttr = 0;
			numAttr = (uint32_t)PyTuple_Size(keywords);
			if (numAttr == 0) {
				PyErr_SetString(PyExc_TypeError, "Parameter error.");
				return NULL;
			}
			const char** paramaters = new const char* [numAttr];
			memset(paramaters, 0, sizeof(char*) * numAttr);
			for (uint32_t i = 0; i < numAttr; i++)
			{
				PyObject* v = PyTuple_GET_ITEM(keywords, i);
				paramaters[i] = PyUnicode_AsUTF8(v);
			}
			self->firebaseAdmob->setKeywords(numAttr, paramaters);
		}

		if (birthday)
		{
			int birthdaySize = firebase::pyObjToIntArray(birthday, nullptr);
			if (birthdaySize != 3) {
				PyErr_SetString(PyExc_TypeError, "3 Parameters : day(int) | month(int) | year(int)");
				return NULL;
			}
			uint32_t* buffer = (uint32_t*)malloc(birthdaySize * sizeof(int));
			firebase::pyObjToIntArray(birthday, buffer);
			self->firebaseAdmob->setBirthday(buffer[0], buffer[1], buffer[2]);
		}

		if (testDevicesIds)
		{
			uint32_t numAttr = 0;
			numAttr = (uint32_t)PyTuple_Size(testDevicesIds);
			if (numAttr == 0) {
				PyErr_SetString(PyExc_TypeError, "Parameter error.");
				return NULL;
			}
			const char** paramaters = new const char* [numAttr];
			memset(paramaters, 0, sizeof(char*) * numAttr);
			for (uint32_t i = 0; i < numAttr; i++)
			{
				PyObject* v = PyTuple_GET_ITEM(testDevicesIds, i);
				paramaters[i] = PyUnicode_AsUTF8(v);
			}
			self->firebaseAdmob->setTestDeviceIds(numAttr, paramaters);
		}
	}

	self->firebaseAdmob->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAdmob_Release(firebaseAdmob_obj* self)
{
	self->firebaseAdmob->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAdmob_Testcase(firebaseAdmob_obj* self)
{
	self->firebaseAdmob->testcase();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAdmob_ShowBanner(firebaseAdmob_obj* self, PyObject* args)
{
	PyObject* reload = nullptr;
	PyObject* timeout = nullptr;

	if (!PyArg_ParseTuple(args, "|OO", &reload, &timeout)) return NULL;
	if (!reload)
	{
		self->firebaseAdmob->showBanner();
	}
	else
	{
		if (!timeout)
		{
			self->firebaseAdmob->showBanner((bool)PyLong_AsLong(reload));
		}
		else
		{
			self->firebaseAdmob->showBanner((bool)PyLong_AsLong(reload), (int)PyLong_AsLong(timeout));
		}
	}	

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAdmob_BannerMoveTo(firebaseAdmob_obj* self, PyObject* args)
{	
	/// Top of the screen, horizontally centered. -> kPositionTop = 0,
	/// Bottom of the screen, horizontally centered. ->	kPositionBottom,
	/// Top-left corner of the screen. -> kPositionTopLeft,
	/// Top-right corner of the screen. -> kPositionTopRight,
	/// Bottom-left corner of the screen. -> kPositionBottomLeft,
	/// Bottom-right corner of the screen. -> kPositionBottomRight,

	PyObject* firstParameter = nullptr;
	PyObject* secondParameter = nullptr;

	if (!PyArg_ParseTuple(args, "O|O", &firstParameter, &secondParameter)) return NULL;
	if (secondParameter && PyLong_Check(firstParameter) && PyLong_Check(secondParameter))
	{
		int x = PyLong_AsLong(firstParameter);
		int y = PyLong_AsLong(secondParameter);
		self->firebaseAdmob->bannerMoveTo(x, y);
	}
	else if (firstParameter && PyLong_Check(firstParameter))
	{
		int position = PyLong_AsLong(firstParameter);
		self->firebaseAdmob->bannerMoveTo((admob::BannerView::Position)position);		
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAdmob_HideBanner(firebaseAdmob_obj* self)
{
	self->firebaseAdmob->hideBanner();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAdmob_ShowInterstitial(firebaseAdmob_obj* self, PyObject* args)
{
	PyObject* reload = nullptr;
	PyObject* timeout = nullptr;
	
	if (!PyArg_ParseTuple(args, "|OO", &reload, &timeout)) return NULL;
	if (!reload)
	{
		self->firebaseAdmob->showInterstitial();
	}
	else
	{
		if (!timeout)
		{
			self->firebaseAdmob->showInterstitial((bool)PyLong_AsLong(reload));
		}
		else
		{
			self->firebaseAdmob->showInterstitial((bool)PyLong_AsLong(reload), (int)PyLong_AsLong(timeout));
		}
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAdmob_ShowRewardedVideo(firebaseAdmob_obj* self, PyObject* args)
{
	PyObject* reload = nullptr;
	PyObject* timeout = nullptr;

	if (!PyArg_ParseTuple(args, "|OO", &reload, &timeout)) return NULL;
	if (!reload)
	{
		self->firebaseAdmob->showRewardedVideo();
	}
	else
	{
		if (!timeout)
		{
			self->firebaseAdmob->showRewardedVideo((bool)PyLong_AsLong(reload));
		}
		else
		{
			self->firebaseAdmob->showRewardedVideo((bool)PyLong_AsLong(reload), (int)PyLong_AsLong(timeout));
		}
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAdmob_PauseRewardedVideo(firebaseAdmob_obj* self)
{
	self->firebaseAdmob->pauseRewardedVideo();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseAdmob_ResumeRewardedVideo(firebaseAdmob_obj* self)
{
	self->firebaseAdmob->resumeRewardedVideo();

	Py_INCREF(Py_None);
	return Py_None;
}

PyMethodDef firebaseAdmob_methods[] = {
	{ "init", (PyCFunction)firebaseAdmob_Init, METH_VARARGS | METH_KEYWORDS, firebaseAdmobInit_doc },
	{ "release", (PyCFunction)firebaseAdmob_Release, METH_NOARGS, firebaseAdmobRelease_doc },
	{ "testcase", (PyCFunction)firebaseAdmob_Testcase, METH_NOARGS, firebaseAdmobTestcase_doc },
	{ "showBanner", (PyCFunction)firebaseAdmob_ShowBanner, METH_VARARGS, firebaseAdmobShowBanner_doc },
	{ "bannerMoveTo", (PyCFunction)firebaseAdmob_BannerMoveTo, METH_VARARGS, firebaseAdmobBannerMoveTo_doc },
	{ "hideBanner", (PyCFunction)firebaseAdmob_HideBanner, METH_NOARGS, firebaseAdmobHideBanner_doc },
	{ "showInterstitial", (PyCFunction)firebaseAdmob_ShowInterstitial, METH_VARARGS, firebaseAdmobShowInterstitial_doc },
	{ "showRewardedVideo", (PyCFunction)firebaseAdmob_ShowRewardedVideo, METH_VARARGS, firebaseAdmobShowRewardedVideo_doc },
	{ "pauseRewardedVideo", (PyCFunction)firebaseAdmob_PauseRewardedVideo, METH_NOARGS, firebaseAdmobPauseRewardedVideo_doc },
	{ "resumeRewardedVideo", (PyCFunction)firebaseAdmob_ResumeRewardedVideo, METH_NOARGS, firebaseAdmobResumeRewardedVideo_doc },
	{ NULL,	NULL }
};

PyGetSetDef firebaseAdmob_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject FirebaseAdmobType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igefirebase.admob",						/* tp_name */
	sizeof(firebase_obj),						/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)firebaseAdmob_dealloc,			/* tp_dealloc */
	0,											/* tp_print */
	0,											/* tp_getattr */
	0,											/* tp_setattr */
	0,											/* tp_reserved */
	0,											/* tp_repr */
	0,											/* tp_as_number */
	0,											/* tp_as_sequence */
	0,											/* tp_as_mapping */
	0,											/* tp_hash */
	0,											/* tp_call */
	(reprfunc)firebaseAdmob_str,				/* tp_str */
	0,											/* tp_getattro */
	0,											/* tp_setattro */
	0,											/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,							/* tp_flags */
	0,											/* tp_doc */
	0,											/* tp_traverse */
	0,											/* tp_clear */
	0,											/* tp_richcompare */
	0,											/* tp_weaklistoffset */
	0,											/* tp_iter */
	0,											/* tp_iternext */
	firebaseAdmob_methods,					/* tp_methods */
	0,											/* tp_members */
	firebaseAdmob_getsets,					/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	firebaseAdmob_new,							/* tp_new */
	0,											/* tp_free */
};