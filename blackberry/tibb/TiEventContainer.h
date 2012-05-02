/**
 * Appcelerator Titanium Mobile
 * Copyright (c) 2009-2012 by Appcelerator, Inc. All Rights Reserved.
 * Licensed under the terms of the Apache Public License
 * Please see the LICENSE included with this distribution for details.
 */

#ifndef TIEVENTCONTAINER_H_
#define TIEVENTCONTAINER_H_

class TiEvent;

/*
 * TiEvent
 *
 * Abstract class manages a list of subscribers for a specified event
 *
 */

class TiEventContainer
{
public:
    virtual void addListener(TiEvent* listener) = 0;
    virtual void fireEvent() = 0;
    virtual void setDataProperty(const char* propertyName, const char* value) = 0;
    virtual void setDataProperty(const char* propertyName, int value) = 0;
    virtual void setDataProperty(const char* propertyName, float value) = 0;
    virtual ~TiEventContainer()
    {
    }
    ;

protected:
    TiEventContainer()
    {
    }
    ;
};

#endif /* TIEVENTCONTAINER_H_ */
