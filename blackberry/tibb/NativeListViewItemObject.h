/**
 * Appcelerator Titanium Mobile
 * Copyright (c) 2009-2012 by Appcelerator, Inc. All Rights Reserved.
 * Licensed under the terms of the Apache Public License
 * Please see the LICENSE included with this distribution for details.
 */

#ifndef NATIVELISTVIEWITEM_H_
#define NATIVELISTVIEWITEM_H_

namespace bb
{
namespace cascades
{
class StandardListItem;
}
}

#include "NativeControlObject.h"

/*
 * NativeListViewItemObject
 *
 * UI: List Item
 */

class NativeListViewItemObject : public NativeControlObject
{
public:
    static NativeListViewItemObject* createListItem();
    virtual NAHANDLE getNativeHandle() const;
    virtual int getObjectType() const;
    virtual int initialize();
    virtual int setTitle(TiObject* obj);
    virtual int setLeftImage(TiObject* obj);

protected:
    virtual ~NativeListViewItemObject();

private:
    NativeListViewItemObject();
    // Disable copy ctor & assignment operator
    NativeListViewItemObject(const NativeListViewItemObject&);
    NativeListViewItemObject& operator=(const NativeListViewItemObject&);
    bb::cascades::StandardListItem* listItem_;
};

#endif /* NATIVELISTVIEWITEM_H_ */
