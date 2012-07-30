/**
 * Appcelerator Titanium Mobile
 * Copyright (c) 2009-2012 by Appcelerator, Inc. All Rights Reserved.
 * Licensed under the terms of the Apache Public License
 * Please see the LICENSE included with this distribution for details.
 */

#include "NativeListViewItemObject.h"
#include <bb/cascades/StandardListItem>

NativeListViewItemObject::NativeListViewItemObject()
{
    listItem_ = NULL;
}

NativeListViewItemObject::~NativeListViewItemObject()
{
}

NativeListViewItemObject* NativeListViewItemObject::createListItem()
{
    return new NativeListViewItemObject;
}

int NativeListViewItemObject::getObjectType() const
{
    return N_TYPE_LIST_ITEM;
}

int NativeListViewItemObject::initialize()
{
    listItem_ = bb::cascades::StandardListItem::create();
    return NATIVE_ERROR_OK;
}

NAHANDLE NativeListViewItemObject::getNativeHandle() const
{
    return listItem_;
}

int NativeListViewItemObject::setTitle(TiObject* obj)
{
    QString str;
    int error = NativeControlObject::getString(obj, str);
    if (error != NATIVE_ERROR_OK)
    {
        return error;
    }
    listItem_->setTitle(str);
    return NATIVE_ERROR_OK;
}

int NativeListViewItemObject::setLeftImage(TiObject* obj)
{
    QString str;
    int error = NativeControlObject::getString(obj, str);
    if (!N_SUCCEEDED(error))
    {
        return error;
    }
    const bb::cascades::Image image = bb::cascades::Image(QUrl("assets" + str));
    listItem_->setImage(image);
    return NATIVE_ERROR_OK;
}
