/**
 * Appcelerator Titanium Mobile
 * Copyright (c) 2009-2012 by Appcelerator, Inc. All Rights Reserved.
 * Licensed under the terms of the Apache Public License
 * Please see the LICENSE included with this distribution for details.
 */

#include "NativeAbstractTextControlObject.h"
#include <bb/cascades/controls/abstracttextcontrol.h>
#include <QMap>
#include <QString>

#define FONT_FAMILY         "fontFamily"
#define FONT_SIZE           "fontSize"
#define FONT_STYLE          "fontStyle"
#define FONT_STYLE_NORMAL   "normal"
#define FONT_STYLE_ITALIC   "italic"
#define FONT_WEIGHT         "fontWeight"
#define FONT_WEIGHT_NORMAL  "normal"
#define FONT_WEIGHT_BOLD    "bold"

NativeAbstractTextControlObject::NativeAbstractTextControlObject()
{
    textControl_ = NULL;
}

NativeAbstractTextControlObject::~NativeAbstractTextControlObject()
{
}

bb::cascades::AbstractTextControl* NativeAbstractTextControlObject::getTextControl() const
{
    return textControl_;
}

void NativeAbstractTextControlObject::setTextControl(bb::cascades::AbstractTextControl* textControl)
{
    textControl_ = textControl;
    setControl((bb::cascades::Control*)textControl_);
}

int NativeAbstractTextControlObject::setText(TiObject* obj)
{
    QString str;
    int error = NativeControlObject::getString(obj, str);
    if (error != NATIVE_ERROR_OK)
    {
        return error;
    }
    textControl_->setText(str);
    return NATIVE_ERROR_OK;
}

int NativeAbstractTextControlObject::setColor(TiObject* obj)
{
    float r;
    float g;
    float b;
    float a;

    int error = NativeControlObject::getColorComponents(obj, &r, &g, &b, &a);
    if (error != NATIVE_ERROR_OK)
    {
        return error;
    }
    bb::cascades::Color cscolor = bb::cascades::Color::fromRGBA(r, g, b, a);
    textControl_->textStyle()->setColor(cscolor);
    return NATIVE_ERROR_OK;
}

int NativeAbstractTextControlObject::setTextAlign(TiObject* obj)
{
    int value;
    int error = NativeControlObject::getInteger(obj, &value);
    if (error != NATIVE_ERROR_OK)
    {
        return error;
    }

    switch (value)
    {
    case TEXT_ALIGNMENT_LEFT:
        textControl_->textStyle()->setAlignment(bb::cascades::TextAlignment::ForceLeft);
        break;
    case TEXT_ALIGNMENT_CENTER:
        textControl_->textStyle()->setAlignment(bb::cascades::TextAlignment::Center);
        break;
    case TEXT_ALIGNMENT_RIGHT:
        textControl_->textStyle()->setAlignment(bb::cascades::TextAlignment::ForceRight);
        break;
    default:
        break;
    }

    return NATIVE_ERROR_OK;
}

int NativeAbstractTextControlObject::setFont(TiObject* obj)
{
    QMap<QString, QString> font;
    int error = NativeControlObject::getMapObject(obj, font);
    if (error != NATIVE_ERROR_OK)
    {
        return error;
    }

    QMap<QString, QString>::const_iterator it = font.begin();
    for (; it != font.end(); ++it)
    {
        if (it.key().compare(FONT_FAMILY) == 0)
        {
            textControl_->textStyle()->setFontFamily(it.value());
        }
        else if (it.key().compare(FONT_SIZE) == 0)
        {
            bool bSucceeded;
            float size = it.value().toFloat(&bSucceeded);
            if (bSucceeded)
            {
                textControl_->textStyle()->setSize(size);
            }
        }
        else if (it.key().compare(FONT_STYLE) == 0)
        {
            if (it.value().compare(FONT_STYLE_NORMAL) == 0)
            {
                textControl_->textStyle()->setFontStyle(bb::cascades::FontStyle::Normal);
            }
            else if (it.value().compare(FONT_STYLE_ITALIC) == 0)
            {
                textControl_->textStyle()->setFontStyle(bb::cascades::FontStyle::Italic);
            }
        }
        else if (it.key().compare(FONT_WEIGHT) == 0)
        {
            if (it.value().compare(FONT_WEIGHT_NORMAL) == 0)
            {
                textControl_->textStyle()->setFontWeight(bb::cascades::FontWeight::Normal);
            }
            else if (it.value().compare(FONT_WEIGHT_BOLD) == 0)
            {
                textControl_->textStyle()->setFontWeight(bb::cascades::FontWeight::Bold);
            }
        }
    }

    return NATIVE_ERROR_OK;
}
