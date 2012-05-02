/**
 * Appcelerator Titanium Mobile
 * Copyright (c) 2009-2012 by Appcelerator, Inc. All Rights Reserved.
 * Licensed under the terms of the Apache Public License
 * Please see the LICENSE included with this distribution for details.
 */

#include "NativeContainerObject.h"
#include <bb/cascades/Container>
#include <bb/cascades/DockLayout>
#include <bb/cascades/DockLayoutProperties>
#include <bb/cascades/Stacklayout>
#include <bb/cascades/Label>
#include <bb/cascades/Button>
#include <bb/cascades/Slider>
#include <bb/cascades/Color>
#include <bb/cascades/ProgressIndicator>
#include <qtgui/QColor>
#include "NativeObjectFactory.h"

using namespace bb::cascades;

NativeContainerObject::NativeContainerObject()
{
    container_ = NULL;
    nativeObjectFactory_ = NULL;
}

NativeContainerObject::NativeContainerObject(Container* container)
{
    container_ = container;
    nativeObjectFactory_ = NULL;
}

NativeContainerObject::~NativeContainerObject()
{
}

NativeObject* NativeContainerObject::createContainer(NativeObjectFactory* nativeObjectFactory)
{
    NativeContainerObject* obj = new NativeContainerObject;
    obj->nativeObjectFactory_ = nativeObjectFactory;
    return obj;
}

int NativeContainerObject::getObjectType() const
{
    return N_TYPE_CONTAINER;
}

NAHANDLE NativeContainerObject::getNativeHandle() const
{
    return container_;
}

int NativeContainerObject::initialize(TiEventContainerFactory* containerFactory)
{
    container_ = Container::create();
    if (container_ == NULL)
    {
        return NATIVE_ERROR_OUTOFMEMORY;
    }
    //container_->setLayout(StackLayout::create());
    return NATIVE_ERROR_OK;
}

int NativeContainerObject::addChildNativeObject(NativeObject* obj)
{
    switch (obj->getObjectType())
    {
    case N_TYPE_CONTAINER:

    case N_TYPE_WINDOW:

    {
        bb::cascades::Container* container = (bb::cascades::Container*) obj->getNativeHandle();
        container_->add(container);
        return NATIVE_ERROR_OK;
    }

    case N_TYPE_LABEL:
    {
        bb::cascades::Label* label = (bb::cascades::Label*) obj->getNativeHandle();
        container_->add(label);
        return NATIVE_ERROR_OK;
    }

    case N_TYPE_BUTTON:

    {
        bb::cascades::Button* button = (bb::cascades::Button*) obj->getNativeHandle();
        container_->add(button);
        return NATIVE_ERROR_OK;
    }

    case N_TYPE_SLIDER:

    {
        bb::cascades::Slider* slider = (bb::cascades::Slider*) obj->getNativeHandle();
        container_->add(slider);
        return NATIVE_ERROR_OK;
    }

    case N_TYPE_PROGRESSBAR:

    {
        bb::cascades::ProgressIndicator* progressIndicator = (bb::cascades::ProgressIndicator*) obj->getNativeHandle();
        container_->add(progressIndicator);
        return NATIVE_ERROR_OK;
    }

    }
    return NATIVE_ERROR_NOTSUPPORTED;
}

int NativeContainerObject::open()
{
    container_->setLayout(new DockLayout());
    nativeObjectFactory_->setRootContainer(this);
    return NATIVE_ERROR_OK;
}

int NativeContainerObject::setBackgroundColor(const char* text)
{
    QString colorString = text;
    QColor color;
    color.setNamedColor(colorString);
    qreal r, g, b, a;
    color.getRgbF(&r, &g, &b, &a);
    Color cscolor = Color::fromRGBA(r, g, b, a);
    container_->setBackground(cscolor);
    return NATIVE_ERROR_OK;
}
