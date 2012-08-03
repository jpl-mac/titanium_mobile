/**
 * Appcelerator Titanium Mobile
 * Copyright (c) 2009-2012 by Appcelerator, Inc. All Rights Reserved.
 * Licensed under the terms of the Apache Public License
 * Please see the LICENSE included with this distribution for details.
 */

#ifndef TIUITABLEVIEWROW_H_
#define TIUITABLEVIEWROW_H_

#include "TiUIBase.h"

/*
 * TiUITableViewRow
 *
 * Represents a Titanium TableViewRow object
 *
 * This object can be created by:
 * Titanium.UI.createTableViewRow({...});
 */
class TiUITableViewRow : public TiUIBase
{
public:
    static TiUITableViewRow* createTableViewRow(NativeObjectFactory* nativeObjectFactory);

protected:
    virtual ~TiUITableViewRow();
    virtual void initializeTiObject(TiObject* parentContext);
//    virtual void onCreateStaticMembers();

private:
    TiUITableViewRow();

    // Disable copy ctor & assignment operator
    TiUITableViewRow(const TiUITableViewRow&);
    TiUITableViewRow& operator=(const TiUITableViewRow&);
};

#endif /* TIUITABLEVIEWROW_H_ */
