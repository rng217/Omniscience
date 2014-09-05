#include <Python.h>
#include <stdlib.h>

#define nHeroes 108
double synergy[nHeroes][nHeroes];
double advantage[nHeroes][nHeroes];
double popularity[nHeroes];
double tryhard;
double agency;

int compdouble(const void *a, const void *b) {
  return *(double*)a-*(double*)b;
}

double pseudo_minimax(double* ourPool, double* theirPool, char* mode, int nBans, double score) {
    while(*mode=='{' || *mode=='}') {
        if(*mode=='{') nBans++;
        mode++;
    }
    if(!*mode) return 1;
    if(*mode=='<') {//our pick
        double maxbest=99;
        double best[10]={90,91,92,93,94,95,96,97,98,99};
        for(int i=0;i<nHeroes;i++) {
            if(!ourPool[i]) continue;
            double value;
            if(!mode[1]) {
                value=score*ourPool[i];//could speed up slightly by multiplying score later
                if(isnan(value)) printf("A.\n");
            } else {
                double ourNewPool[nHeroes], theirNewPool[nHeroes];
                for(int j=0; j<nHeroes; j++) {
                    if(theirPool[j]==0 || i==j) {
                        ourNewPool[j]=theirNewPool[j]=0;
                    } else {
                        ourNewPool[j]=ourPool[j]*synergy[i][j];
                        theirNewPool[j]=theirPool[j]*advantage[i][j];
                    }
                }
                value=pseudo_minimax(ourNewPool, theirNewPool, mode+1, nBans,score*ourPool[i]);
                if(isnan(value)) printf("B.\n");
            }
            if(value<maxbest) {
                double newmaxbest=0;
                for(int j=0;j<10;j++) {
                    if(best[j]==maxbest) best[j]=value;
                    if(best[j]>newmaxbest) newmaxbest=best[j];
                }
                maxbest=newmaxbest;
            }
        }
        qsort(best,10,sizeof(best[0]),compdouble);
        double numerator=0,denominator=0,multiplier=1;
        for(int i=0;i<10;i++) {
            numerator+=multiplier/(best[i]+1);
            denominator+=multiplier;
            multiplier*=agency;
        }
        return denominator/numerator-1;
    } else {//their pick
        double results[nHeroes];
        double max1=-98,max2=-99;
        for(int i=0;i<nHeroes;i++) {
            if(!theirPool[i]) continue;
            if(!mode[1]) {
                results[i]=score*theirPool[i]*popularity[i];
            } else {
                double ourNewPool[nHeroes], theirNewPool[nHeroes];
                for(int j=0; j<nHeroes; j++) {
                    if(theirPool[j]==0 || i==j) {
                        ourNewPool[j]=theirNewPool[j]=0;
                    } else {
                        ourNewPool[j]=ourPool[j]/advantage[i][j];
                        theirNewPool[j]=theirPool[j]/synergy[i][j];
                    }
                }
                results[i]=pseudo_minimax(ourNewPool, theirNewPool, mode+1, 0, score*theirPool[i])*popularity[i];
            }
            if(results[i]>max2) {
                if(results[i]>max1) {
                    max2=max1;
                    max1=results[i];
                } else
                    max2=results[i];
            }
        }
        double total=0;
        double denominator=0;
        for(int i=0;i<nHeroes;i++) {
            if(theirPool[i] && (nBans<1 || results[i]!=max1) && (nBans<2 || results[i]!=max2)) {
                total+=popularity[i]/(results[i]+1);
                denominator+=popularity[i];
            }
        }
        if(denominator==0) printf("D.\n");
        return denominator/total-1;
    }
}

static PyObject* load_settings(PyObject *self, PyObject *args) {
    if (!PyArg_ParseTuple(args, "dd",&tryhard,&agency))
        return NULL;
    Py_RETURN_NONE;
}


static PyObject* load_data(PyObject *self, PyObject *args) {
    PyObject* pysynergy,* pyadvantage,* pypopularity;
    if (!PyArg_ParseTuple(args, "O!O!O!",&PyList_Type,&pysynergy,&PyList_Type,&pyadvantage,&PyList_Type,&pypopularity))
        return NULL;
    double poptotal=0;
    for(int i=0;i<nHeroes;i++) synergy[i][i]=PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(pysynergy,i),i));
    for(int i=0;i<nHeroes;i++) {
        for(int j=0;j<nHeroes;j++) {
            if(i==j) continue;
            synergy[i][j]=PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(pysynergy,i),j))/synergy[j][j]/synergy[i][i];
            advantage[i][j]=PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(pyadvantage,j),i))*synergy[j][j]/synergy[i][i];
        }
        poptotal+=PyFloat_AsDouble(PyList_GetItem(pypopularity,i));
    }
    for(int i=0;i<nHeroes;i++) {
        popularity[i]=nHeroes*PyFloat_AsDouble(PyList_GetItem(pypopularity,i))/poptotal;
        //printf("%f\n",popularity[i]);
    }
    Py_RETURN_NONE;
}

static PyObject* analyze(PyObject *self, PyObject *args) {
    PyObject* pypool,* pyallies,* pyenemies;
    char* mode;
    
    if (!PyArg_ParseTuple(args, "O!O!O!s",&PyList_Type,&pypool,&PyList_Type,&pyallies,&PyList_Type,&pyenemies,&mode))
        return NULL;
    
    double ourPool[nHeroes]={0};
    double theirPool[nHeroes]={0};
    for(int i=0;i<PyList_Size(pypool);i++) {
        int hero=PyInt_AsLong(PyList_GetItem(pypool,i));
        ourPool[hero]=1./((1./(synergy[hero][hero]+1.)-.5)*tryhard+.5)-1.;
        theirPool[hero]=1/synergy[hero][hero];
        for(int j=0;j<PyList_Size(pyallies);j++) {//untested
            int ally=PyInt_AsLong(PyList_GetItem(pyallies,j));
            ourPool[hero]*=synergy[ally][ally]*synergy[hero][ally];
            theirPool[hero]/=synergy[ally][ally]*advantage[hero][ally];
        }
        for(int j=0;j<PyList_Size(pyenemies);j++) {//untested
            int enemy=PyInt_AsLong(PyList_GetItem(pyenemies,j));
            ourPool[hero]*=advantage[hero][enemy]/synergy[enemy][enemy];//more dividing?
            theirPool[hero]/=synergy[hero][enemy]/synergy[enemy][enemy];
        }
    }
    PyObject* choiceValues = PyList_New(nHeroes);
    if(*mode=='{') {//our ban
        for(int i=0;i<nHeroes;i++) {
            if(ourPool[i]==0) {
                PyList_SET_ITEM(choiceValues,i,PyFloat_FromDouble(0)); //necessary?
                continue;
            }
            double ourOld=ourPool[i];
            double theirOld=theirPool[i];
            ourPool[i]=theirPool[i]=0;
            PyList_SET_ITEM(choiceValues,i,PyFloat_FromDouble(pseudo_minimax(ourPool,theirPool,mode+1,0,1)));
            ourPool[i]=ourOld;
            theirPool[i]=theirOld;
        }
    } else {//our pick
        double ourNewPool[nHeroes];
        double theirNewPool[nHeroes];
        for(int hero=0;hero<nHeroes;hero++) {
            if(!mode[1] || ourPool[hero]==0) {
                PyList_SET_ITEM(choiceValues,hero,PyFloat_FromDouble(ourPool[hero]));
            } else {
                for(int i=0;i<nHeroes;i++) {
                    if(ourPool[i]==0 || i==hero) {
                        ourNewPool[i]=theirNewPool[i]=0;
                    } else {
                        ourNewPool[i]=ourPool[i]*synergy[hero][i];
                        theirNewPool[i]=theirPool[i]*advantage[hero][i];
                    }
                }
                PyList_SET_ITEM(choiceValues,hero,PyFloat_FromDouble(pseudo_minimax(ourNewPool,theirNewPool,mode+1,0,ourPool[hero])));
            }
        }
    }
    return choiceValues;
}

static PyMethodDef omnisciencemethods[] = {
    {"analyze",  analyze, METH_VARARGS, "Determine hero viability."},
    {"load_data",  load_data, METH_VARARGS, "Load statistical data."},
    {"load_settings",  load_settings, METH_VARARGS, "Load statistical data."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initomnisciencemodule(void) {
    (void) Py_InitModule("omnisciencemodule", omnisciencemethods);
}