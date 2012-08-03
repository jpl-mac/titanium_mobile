/**
 * Appcelerator Titanium Mobile
 * Copyright (c) 2009-2012 by Appcelerator, Inc. All Rights Reserved.
 * Licensed under the terms of the Apache Public License
 * Please see the LICENSE included with this distribution for details.
 */

#include "TiUITableViewRow.h"
#include "TiGenericFunctionObject.h"

TiUITableViewRow::TiUITableViewRow()
    : TiUIBase("")
{
}

TiUITableViewRow::~TiUITableViewRow()
{
}

TiUITableViewRow* TiUITableViewRow::createTableViewRow(NativeObjectFactory* nativeObjectFactory)
{
    TiUITableViewRow* obj = new TiUITableViewRow;
    //obj->setNativeObjectFactory(nativeObjectFactory);
    obj->initializeTiObject(NULL);
    return obj;
}

void TiUITableViewRow::initializeTiObject(TiObject* parentContext)
{
    if (!isInitialized())
    {
        TiUIBase::initializeTiObject(parentContext);
        //NativeObject* obj = getNativeObjectFactory()->createNativeObject(N_TYPE_LIST_ITEM);
        //setNativeObject(obj);
        //obj->release();
    }
}

/*void TiUITableViewRow::onCreateStaticMembers()
{
    TiUIBase::onCreateStaticMembers();
}*/
