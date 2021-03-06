# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from telemetry.internal.actions import page_action
from telemetry.internal.actions import utils

class MouseClickAction(page_action.PageAction):
  def __init__(self, selector=None):
    super(MouseClickAction, self).__init__()
    self._selector = selector

  def WillRunAction(self, tab):
    """Load the mouse click JS code prior to running the action."""
    super(MouseClickAction, self).WillRunAction(tab)
    utils.InjectJavaScript(tab, 'mouse_click.js')
    done_callback = 'function() { window.__mouseClickActionDone = true; }'
    tab.ExecuteJavaScript("""
        window.__mouseClickActionDone = false;
        window.__mouseClickAction = new __MouseClickAction(%s);"""
        % (done_callback))

  def RunAction(self, tab):
    code = '''
        function(element, info) {
          if (!element) {
            throw Error('Cannot find element: ' + info);
          }
          window.__mouseClickAction.start({
            element: element
          });
        }'''
    page_action.EvaluateCallbackWithElement(
        tab, code, selector=self._selector)
    tab.WaitForJavaScriptExpression('window.__mouseClickActionDone', 60)
